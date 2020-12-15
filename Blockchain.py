import Block
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.genesis_block = Block(None, None, None)
        self.last_block = genesis_block
    
