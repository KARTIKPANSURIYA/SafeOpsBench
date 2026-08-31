"""Canonical state snapshot and hashing."""
import hashlib, json
from typing import Any
def state_hash(state:dict[str,Any])->str:
    return hashlib.sha256(json.dumps(state,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
