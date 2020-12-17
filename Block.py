import json
import MerkleTree
from hashlib import sha256
from datetime import datetime

class Block:
    def __init__(self, index: int, data: list, timestamp: datetime, previous_hash: str):
        """
        Constructor for a Block
        @param data             The data stored in the block (JSON)
        @param timestamp        The timestamp
        @param previous_hash    The hash of the previous block
        """
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = '0x'
        self.mtree = MerkleTree('__ROOT_NODE__')
        self.mtree_hash = ''
        self.hash = None
        for entry in data:
            add_transaction(entry)
    def generate_hash(self) -> str:
        mtree_hash = mtree.compute_hash
        self.hash = sha256(nonce + previous_hash + mtree_hash).hexdigest()
        return self.hash
    def add_transaction(self, data: str):
        self.mtree.insert(data)
