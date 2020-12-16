import Block
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.genesis_block = Block(None, datetime.now(), '0')
        genesis_block.generate_hash()
        self.last_block = genesis_block
    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of a latest block
          in the chain match.
        """
        pass
