import json
import MerkleTree

class Block:
    def __init__(self, data: str, timestamp: datetime, previous_hash: str):
        """
        Constructor for a Block
        @param id               The unique id for the block (SHA256)
        @param data             The data stored in the block
        @param timestamp        The timestamp
        @param previous_hash    The hash of the previous block
        """
        self.id = self.generate_hash()
        self.data = data
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = '0x'
        self.mtree = MerkleTree()
        
