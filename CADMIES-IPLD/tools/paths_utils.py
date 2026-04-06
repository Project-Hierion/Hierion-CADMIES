#!/usr/bin/env python3
"""
CAR Utils v1.0.0 - Minimal CAR (Content Addressable Archive) reader/writer
Purpose: Read/write CAR files without external dependencies (uses dag-cbor + multiformats)
Spec: https://ipld.io/specs/transport/car/carv1/
"""

import struct
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import dag_cbor
from multiformats import CID, multihash

# ============================================================================
# LOW-LEVEL CAR FUNCTIONS
# ============================================================================

def calculate_cid(data: bytes, codec: str = "dag-cbor") -> str:
    """
    Calculate CID v1 for given data.
    
    Args:
        data: Raw bytes to hash
        codec: Multicodec codec name (default: dag-cbor)
    
    Returns:
        CID string (e.g., "bafyre...")
    """
    # Hash with SHA2-256
    digest = multihash.digest(data, "sha2-256")
    # Create CID v1 with dag-cbor codec
    cid_obj = CID.create("cidv1", codec, digest)
    return str(cid_obj)


def write_car(blocks: Dict[str, bytes], roots: List[str], output_path: Path) -> None:
    """
    Write blocks to CAR file.
    
    CAR format:
    [header] [block1] [block2] ... [blockN]
    
    Header: DAG-CBOR encoded dict with "version" and "roots"
    Block: [cid_length:varint][cid_bytes][block_length:varint][block_bytes]
    
    Args:
        blocks: Dict of {cid_string: block_bytes}
        roots: List of root CID strings (first blocks to reference)
        output_path: Where to write the CAR file
    """
    with open(output_path, 'wb') as f:
        # 1. Write header
        header = {"version": 1, "roots": roots}
        header_bytes = dag_cbor.encode(header)
        
        # Write header length (varint) then header
        _write_varint(f, len(header_bytes))
        f.write(header_bytes)
        
        # 2. Write each block
        for cid_str, block_data in blocks.items():
            # Parse CID to bytes
            cid_obj = CID.decode(cid_str)
            cid_bytes = cid_obj.encode()
            
            # Write CID length + CID bytes
            _write_varint(f, len(cid_bytes))
            f.write(cid_bytes)
            
            # Write block length + block bytes
            _write_varint(f, len(block_data))
            f.write(block_data)


def read_car(file_path: Path) -> Tuple[Dict[str, bytes], List[str]]:
    """
    Read CAR file and extract all blocks.
    
    Args:
        file_path: Path to CAR file
    
    Returns:
        Tuple of (blocks_dict, roots_list)
        blocks_dict: {cid_string: block_bytes}
        roots_list: List of root CID strings
    """
    blocks = {}
    roots = []
    
    with open(file_path, 'rb') as f:
        # 1. Read header
        header_length = _read_varint(f)
        header_bytes = f.read(header_length)
        header = dag_cbor.decode(header_bytes)
        
        # Validate CAR version
        if header.get("version") != 1:
            raise ValueError(f"Unsupported CAR version: {header.get('version')}")
        
        roots = header.get("roots", [])
        
        # 2. Read blocks until EOF
        while True:
            try:
                # Read CID length
                cid_length = _read_varint(f)
                if cid_length == 0:
                    break
                
                # Read CID bytes
                cid_bytes = f.read(cid_length)
                if len(cid_bytes) != cid_length:
                    break  # EOF or corrupted
                
                # Decode CID
                cid_obj = CID.decode(cid_bytes)
                cid_str = str(cid_obj)
                
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
    """
    Write unsigned 64-bit varint to file.
    
    Format: 7 bits per byte, MSB = 1 for more bytes, 0 for last byte
    """
    while True:
        if value < 0x80:
            file_handle.write(struct.pack('B', value))
            break
        else:
            file_handle.write(struct.pack('B', (value & 0x7F) | 0x80))
            value >>= 7


def _read_varint(file_handle) -> int:
    """
    Read unsigned 64-bit varint from file.
    
    Returns:
        Decoded integer value
    """
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
    """
    Load a block from CADMIES blockstore by CID.
    
    Args:
        cid: CID string
        blocks_dir: Path to store/blocks/
    
    Returns:
        Block bytes or None if not found
    """
    block_path = blocks_dir / f"{cid}.cbor"
    if not block_path.exists():
        return None
    
    with open(block_path, 'rb') as f:
        return f.read()


def save_block_to_store(cid: str, block_data: bytes, blocks_dir: Path) -> bool:
    """
    Save a block to CADMIES blockstore.
    
    Args:
        cid: CID string
        block_data: Raw block bytes
        blocks_dir: Path to store/blocks/
    
    Returns:
        True if saved, False if already exists
    """
    block_path = blocks_dir / f"{cid}.cbor"
    if block_path.exists():
        return False
    
    with open(block_path, 'wb') as f:
        f.write(block_data)
    return True


def verify_block_integrity(block_data: bytes, expected_cid: str) -> bool:
    """
    Verify that block data matches its CID.
    
    Args:
        block_data: Raw block bytes
        expected_cid: Expected CID string
    
    Returns:
        True if CID matches, False otherwise
    """
    actual_cid = calculate_cid(block_data)
    return actual_cid == expected_cid


# ============================================================================
# SELF-TEST (run with python car_utils.py)
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CAR Utils v1.0.0 - Self Test")
    print("=" * 60)
    
    # Test 1: Write and read a simple CAR file
    print("\n1. Testing write/read roundtrip...")
    
    test_blocks = {
        "bafyreib1test1": b"Hello world",
        "bafyreib1test2": b"Second block"
    }
    test_roots = ["bafyreib1test1"]
    
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.car', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    # Write CAR
    write_car(test_blocks, test_roots, tmp_path)
    print(f"   Wrote CAR to {tmp_path}")
    
    # Read CAR
    read_blocks, read_roots = read_car(tmp_path)
    print(f"   Read {len(read_blocks)} blocks, roots: {read_roots}")
    
    # Verify
    success = (len(read_blocks) == 2 and 
               read_blocks.get("bafyreib1test1") == b"Hello world" and
               read_blocks.get("bafyreib1test2") == b"Second block")
    
    if success:
        print("   ✅ Roundtrip successful")
    else:
        print("   ❌ Roundtrip failed")
    
    # Cleanup
    tmp_path.unlink()
    
    # Test 2: CID calculation
    print("\n2. Testing CID calculation...")
    test_data = b'{"test": true}'
    cid = calculate_cid(test_data)
    print(f"   Data: {test_data}")
    print(f"   CID: {cid}")
    
    if cid.startswith('bafy'):
        print("   ✅ CID calculation working")
    else:
        print("   ❌ CID calculation failed")
    
    print("\n" + "=" * 60)
    print("CAR Utils ready for use")
    print("=" * 60)
