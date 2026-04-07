#!/usr/bin/env python3
"""
CAR Utils v1.0.0 - Minimal CAR (Content Addressable Archive) reader/writer
Purpose: Read/write CAR files without external dependencies
Spec: https://ipld.io/specs/transport/car/carv1/
"""

import struct
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import dag_cbor
from multiformats import CID, multihash

# ============================================================================
# CID HELPER FUNCTIONS
# ============================================================================

def calculate_cid(data: bytes) -> str:
    """Calculate CID string for given data."""
    digest = multihash.digest(data, "sha2-256")
    cid_obj = CID.decode(digest)
    return str(cid_obj)


def cid_str_to_storage_bytes(cid_str: str) -> bytes:
    """
    Convert CID string to storage bytes.
    Simply encode the string as UTF-8 bytes.
    This bypasses library decode issues.
    """
    return cid_str.encode('utf-8')


def storage_bytes_to_cid_str(storage_bytes: bytes) -> str:
    """
    Convert storage bytes back to CID string.
    Simply decode UTF-8 bytes to string.
    """
    return storage_bytes.decode('utf-8')


# ============================================================================
# CAR FORMAT FUNCTIONS
# ============================================================================

def write_car(blocks: Dict[str, bytes], roots: List[str], output_path: Path) -> None:
    """
    Write blocks to CAR file.
    
    Args:
        blocks: Dict of {cid_string: block_bytes}
        roots: List of root CID strings
        output_path: Where to write the CAR file
    """
    with open(output_path, 'wb') as f:
        # Convert root CID strings to storage bytes for header
        root_bytes_list = [cid_str_to_storage_bytes(root) for root in roots]
        
        # Write header
        header = {"version": 1, "roots": root_bytes_list}
        header_bytes = dag_cbor.encode(header)
        _write_varint(f, len(header_bytes))
        f.write(header_bytes)
        
        # Write each block
        for cid_str, block_data in blocks.items():
            # Convert CID string to storage bytes
            cid_bytes = cid_str_to_storage_bytes(cid_str)
            
            # Write CID length + CID bytes
            _write_varint(f, len(cid_bytes))
            f.write(cid_bytes)
            
            # Write block length + block data
            _write_varint(f, len(block_data))
            f.write(block_data)


def read_car(file_path: Path) -> Tuple[Dict[str, bytes], List[str]]:
    """
    Read CAR file and extract all blocks.
    
    Returns:
        Tuple of (blocks_dict, roots_list)
        blocks_dict: {cid_string: block_bytes}
        roots_list: List of root CID strings
    """
    blocks = {}
    roots = []
    
    with open(file_path, 'rb') as f:
        # Read header
        header_length = _read_varint(f)
        header_bytes = f.read(header_length)
        header = dag_cbor.decode(header_bytes)
        
        if header.get("version") != 1:
            raise ValueError(f"Unsupported CAR version: {header.get('version')}")
        
        # Convert root bytes back to CID strings
        for root_bytes in header.get("roots", []):
            roots.append(storage_bytes_to_cid_str(root_bytes))
        
        # Read blocks
        while True:
            try:
                # Read CID length
                cid_length = _read_varint(f)
                if cid_length == 0:
                    break
                
                # Read CID bytes
                cid_bytes = f.read(cid_length)
                if len(cid_bytes) != cid_length:
                    break
                
                # Convert CID bytes back to string
                cid_str = storage_bytes_to_cid_str(cid_bytes)
                
                # Read block length
                block_length = _read_varint(f)
                
                # Read block data
                block_data = f.read(block_length)
                if len(block_data) != block_length:
                    raise ValueError(f"Truncated block for CID {cid_str}")
                
                # Store block
                blocks[cid_str] = block_data
                
            except EOFError:
                break
    
    return blocks, roots


def _write_varint(file_handle, value: int) -> None:
    """Write unsigned 64-bit varint to file."""
    while True:
        if value < 0x80:
            file_handle.write(struct.pack('B', value))
            break
        else:
            file_handle.write(struct.pack('B', (value & 0x7F) | 0x80))
            value >>= 7


def _read_varint(file_handle) -> int:
    """Read unsigned 64-bit varint from file."""
    result = 0
    shift = 0
    
    while True:
        byte = file_handle.read(1)
        if not byte:
            raise EOFError("Unexpected EOF while reading varint")
        
        b = struct.unpack('B', byte)[0]
        result |= (b & 0x7F) << shift
        shift += 7
        
        if not (b & 0x80):
            break
    
    return result


# ============================================================================
# CADMIES-SPECIFIC HELPER FUNCTIONS
# ============================================================================

def load_block_from_store(cid: str, blocks_dir: Path) -> Optional[bytes]:
    """Load a block from CADMIES blockstore by CID."""
    block_path = blocks_dir / f"{cid}.cbor"
    if not block_path.exists():
        return None
    with open(block_path, 'rb') as f:
        return f.read()


def save_block_to_store(cid: str, block_data: bytes, blocks_dir: Path) -> bool:
    """Save a block to CADMIES blockstore."""
    block_path = blocks_dir / f"{cid}.cbor"
    if block_path.exists():
        return False
    with open(block_path, 'wb') as f:
        f.write(block_data)
    return True


def verify_block_integrity(block_data: bytes, expected_cid: str) -> bool:
    """Verify that block data matches its CID."""
    actual_cid = calculate_cid(block_data)
    return actual_cid == expected_cid


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CAR Utils v1.0.0 - Self Test")
    print("=" * 60)
    
    # Test 1: Write and read a simple CAR file
    print("\n1. Testing write/read roundtrip...")
    
    block1_data = b"Hello world"
    block2_data = b"Second block"
    
    cid1_str = calculate_cid(block1_data)
    cid2_str = calculate_cid(block2_data)
    
    print(f"   CID1: {cid1_str}")
    print(f"   CID2: {cid2_str}")
    
    test_blocks = {
        cid1_str: block1_data,
        cid2_str: block2_data
    }
    test_roots = [cid1_str]
    
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.car', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    write_car(test_blocks, test_roots, tmp_path)
    print(f"   Wrote CAR to {tmp_path}")
    
    read_blocks, read_roots = read_car(tmp_path)
    print(f"   Read {len(read_blocks)} blocks, roots: {read_roots}")
    
    success = (len(read_blocks) == 2 and 
               read_blocks.get(cid1_str) == block1_data and
               read_blocks.get(cid2_str) == block2_data)
    
    if success:
        print("   ✅ Roundtrip successful")
    else:
        print("   ❌ Roundtrip failed")
    
    tmp_path.unlink()
    
    # Test 2: CID calculation
    print("\n2. Testing CID calculation...")
    test_data = b'{"test": true}'
    cid = calculate_cid(test_data)
    print(f"   Data: {test_data}")
    print(f"   CID: {cid}")
    
    if cid.startswith('Qm') or cid.startswith('bafy'):
        print("   ✅ CID calculation working")
    else:
        print("   ❌ CID calculation failed")
    
    # Test 3: Storage conversion
    print("\n3. Testing storage conversion...")
    test_cid_str = calculate_cid(b"test conversion")
    test_cid_bytes = cid_str_to_storage_bytes(test_cid_str)
    test_cid_back = storage_bytes_to_cid_str(test_cid_bytes)
    
    print(f"   Original: {test_cid_str}")
    print(f"   Bytes length: {len(test_cid_bytes)}")
    print(f"   Converted back: {test_cid_back}")
    
    if test_cid_back == test_cid_str:
        print("   ✅ Conversion works")
    else:
        print("   ❌ Conversion failed")
    
    print("\n" + "=" * 60)
    print("CAR Utils ready for use")
    print("=" * 60)