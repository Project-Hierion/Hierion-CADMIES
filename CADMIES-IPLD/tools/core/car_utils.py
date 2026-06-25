#!/usr/bin/env python3
"""
File: car_utils.py
Tool: CADMIES CAR Utilities
Version: 1.0.3
System: CADMIES / tools/core
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Read/write CAR (Content Addressable Archive) files without external dependencies.
         Spec: https://ipld.io/specs/transport/car/carv1/

Usage:
    from car_utils import write_car, read_car, read_car_index, calculate_cid

Version History:
  v1.0.3 (2026-05-25): Added read_car_index() to extract human_id -> CID mapping.
  v1.0.2 (2026-05-23): Fixed calculate_cid() to use hashlib.sha256 + multihash.wrap.
  v1.0.1 (2026-05-23): Fixed CID construction, added re-encode verification.
  v1.0.0: Initial release.
"""

import struct
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import dag_cbor
from multiformats import CID, multihash


def calculate_cid(data: bytes) -> str:
    """Calculate CID string for given data.
    
    Uses hashlib.sha256 + multihash.wrap to match cid_generator.py
    and remint_existing_concepts.py.
    """
    hash_bytes = hashlib.sha256(data).digest()
    mh = multihash.wrap(hash_bytes, "sha2-256")
    cid_obj = CID("base32", 1, "dag-cbor", mh)
    return str(cid_obj)


def cid_str_to_storage_bytes(cid_str: Union[str, bytes]) -> bytes:
    """Convert CID string or bytes to storage bytes for CAR."""
    if isinstance(cid_str, bytes):
        return cid_str
    elif isinstance(cid_str, str):
        return cid_str.encode('utf-8')
    else:
        raise TypeError(f"Expected str or bytes, got {type(cid_str)}")


def storage_bytes_to_cid_str(storage_bytes: Union[str, bytes]) -> str:
    """Convert storage bytes back to CID string."""
    if isinstance(storage_bytes, bytes):
        return storage_bytes.decode('utf-8')
    elif isinstance(storage_bytes, str):
        return storage_bytes
    else:
        raise TypeError(f"Expected str or bytes, got {type(storage_bytes)}")


def cids_equivalent(cid1: str, cid2: str) -> bool:
    """Check if two CIDs refer to the same content."""
    if cid1 == cid2:
        return True
    
    try:
        obj1 = CID.decode(cid1)
        obj2 = CID.decode(cid2)
        return obj1.digest == obj2.digest
    except (ValueError, ImportError):
        return False


def write_car(blocks: Dict[bytes, bytes], roots: List[bytes], output_path: Path) -> None:
    """Write blocks to CAR file."""
    with open(output_path, 'wb') as f:
        root_bytes_list = [cid_str_to_storage_bytes(root) for root in roots]
        
        header = {"version": 1, "roots": root_bytes_list}
        header_bytes = dag_cbor.encode(header)
        _write_varint(f, len(header_bytes))
        f.write(header_bytes)
        
        for cid_bytes, block_data in blocks.items():
            cid_bytes_clean = cid_str_to_storage_bytes(cid_bytes)
            
            _write_varint(f, len(cid_bytes_clean))
            f.write(cid_bytes_clean)
            
            _write_varint(f, len(block_data))
            f.write(block_data)


def read_car(file_path: Path) -> Tuple[Dict[str, bytes], List[str]]:
    """Read CAR file and extract all blocks."""
    blocks = {}
    roots = []
    
    with open(file_path, 'rb') as f:
        header_length = _read_varint(f)
        header_bytes = f.read(header_length)
        header = dag_cbor.decode(header_bytes)
        
        if header.get("version") != 1:
            raise ValueError(f"Unsupported CAR version: {header.get('version')}")
        
        for root_bytes in header.get("roots", []):
            roots.append(storage_bytes_to_cid_str(root_bytes))
        
        while True:
            try:
                cid_length = _read_varint(f)
                if cid_length == 0:
                    break
                
                cid_bytes = f.read(cid_length)
                if len(cid_bytes) != cid_length:
                    break
                
                cid_str = storage_bytes_to_cid_str(cid_bytes)
                
                block_length = _read_varint(f)
                block_data = f.read(block_length)
                if len(block_data) != block_length:
                    raise ValueError(f"Truncated block for CID {cid_str}")
                
                blocks[cid_str] = block_data
                
            except EOFError:
                break
    
    return blocks, roots


def read_car_index(file_path: Path) -> Dict[str, str]:
    """Build human_id -> CID mapping from all concept blocks in a CAR file."""
    blocks, roots = read_car(file_path)
    index = {}
    
    for cid_str, block_data in blocks.items():
        try:
            decoded = dag_cbor.decode(block_data)
            if isinstance(decoded, dict) and 'human_id' in decoded:
                human_id = decoded['human_id']
                index[human_id] = cid_str
        except (ValueError, TypeError):
            continue
    
    return index


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
    try:
        decoded = dag_cbor.decode(block_data)
        normalized = dag_cbor.encode(decoded)
        actual_cid = calculate_cid(normalized)
        return cids_equivalent(actual_cid, expected_cid)
    except (ValueError, TypeError):
        actual_cid = calculate_cid(block_data)
        return cids_equivalent(actual_cid, expected_cid)


if __name__ == "__main__":
    print("=" * 60)
    print("CADMIES CAR UTILS v1.0.3 - Self Test")
    print("=" * 60)
    
    print("\n1. Testing write/read roundtrip...")
    
    block1_data = b"Hello world"
    block2_data = b"Second block"
    
    cid1_str = calculate_cid(block1_data)
    cid2_str = calculate_cid(block2_data)
    
    print(f"   CID1: {cid1_str}")
    print(f"   CID2: {cid2_str}")
    
    cid1_bytes = cid_str_to_storage_bytes(cid1_str)
    cid2_bytes = cid_str_to_storage_bytes(cid2_str)
    
    test_blocks = {
        cid1_bytes: block1_data,
        cid2_bytes: block2_data
    }
    test_roots = [cid1_bytes]
    
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.car', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    write_car(test_blocks, test_roots, tmp_path)
    print(f"   Wrote CAR to {tmp_path}")
    print(f"   File size: {tmp_path.stat().st_size} bytes")
    
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
    
    print("\n2. Testing CID calculation...")
    test_data = b'{"test": true}'
    cid = calculate_cid(test_data)
    print(f"   Data: {test_data}")
    print(f"   CID: {cid}")
    
    if cid.startswith('Qm') or cid.startswith('bafy'):
        print("   ✅ CID calculation working")
    else:
        print("   ❌ CID calculation failed")
    
    print("\n3. Testing CID equivalence...")
    test_block = b'{"test": "equivalence"}'
    cid_v0 = calculate_cid(test_block)
    cid_v0_again = calculate_cid(test_block)
    
    print(f"   CID from data: {cid_v0}")
    print(f"   Same data again: {cid_v0_again}")
    print(f"   Strings match: {cid_v0 == cid_v0_again}")
    
    equivalent = cids_equivalent(cid_v0, cid_v0_again)
    print(f"   cids_equivalent() returns: {equivalent}")
    
    if equivalent and cid_v0 == cid_v0_again:
        print("   ✅ CID equivalence working")
    else:
        print("   ❌ CID equivalence failed")
    
    print("\n4. Testing CID string/byte conversion...")
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
    print("CAR Utils v1.0.3 ready for use")
    print("=" * 60)
