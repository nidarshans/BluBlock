import json
from MerkleTree import MerkleTree
from hashlib import sha256
from datetime import datetime

class Block:
    def __init__(self, index: int, data: list, timestamp: str, previous_hash: str, nonce: str):
        """
        Constructor for a Block
        @param data             The data stored in the block
        @param timestamp        The timestamp
        @param previous_hash    The hash of the previous block
        """
        '''
        self.index = index
        self.timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        self.previous_hash = previous_hash
        '''
        self.block_data = dict()
        self.block_data['index'] = index
        self.block_data['timestamp'] = timestamp
        self.block_data['previous_hash'] = previous_hash
        self.block_data['nonce'] = nonce
        self.block_data['hash'] = ''
        self.block_data['data'] = data
        self.mtree = MerkleTree('__ROOT_NODE__')
        for i in data:
            self.mtree.insert(i)
    def generate_hash(self, force: bool) -> str:
        if force:
            mtree_hash = self.mtree.force_compute_hash()
        else:
            mtree_hash = self.mtree.compute_hash()
        data = self.block_data['nonce'] + self.block_data['previous_hash'] + \
            self.mtree.root.hash + self.block_data['timestamp']
        self.block_data['hash'] = sha256(data.encode('utf-8')).hexdigest()
        return self.block_data['hash']
    def add_transaction(self, data: str):
        self.block_data['data'].append(data)
        self.mtree.insert(data)
