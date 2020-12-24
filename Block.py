import json
from MerkleTree import MerkleTree
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
        self.timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        self.previous_hash = previous_hash
        self.nonce = '0x'
        self.mtree = MerkleTree('__ROOT_NODE__')
        self.hash = None
        for entry in data:
            self.mtree.insert(entry)
    def generate_hash(self) -> str:
        mtree_hash = self.mtree.compute_hash()
        data = self.nonce + self.previous_hash + self.mtree.root.hash + self.timestamp
        self.hash = sha256(data.encode('utf-8')).hexdigest()
        return self.hash
    def add_transaction(self, data: str):
        self.mtree.insert(data)
