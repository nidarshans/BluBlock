import json
import MerkleTree

class Block:
    def __init__(self, data: str, timestamp: datetime, previous_hash: str, previous_block: Block):
        """
        Constructor for a Block
        @param data             The data stored in the block (JSON)
        @param timestamp        The timestamp
        @param previous_hash    The hash of the previous block
        """
        self.id = ''
        self.data = data
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.previous_block = previous_block
        self.nonce = '0x'
        self.mtree = MerkleTree(data)
        self.hash = None
    def generate_hash(self):
        self.hash = mtree.compute_hash()
    def add_transaction(self, data: str):
        self.mtree.insert(data)
