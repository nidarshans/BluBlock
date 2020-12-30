from Block import Block
from datetime import datetime
import json

class Blockchain:
    difficulty = 3
    index = 0
    def __init__(self):
        self.genesis_block = Block(0, [json.dumps({'signature': 'GENESIS'})],
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), '0', '0x')
        self.genesis_block.generate_hash(False)
        self.chain = [self.genesis_block]
        self.unconfirmed_transactions = []
        Blockchain.index += 1
    def proof_of_work(self, block: Block) -> Block:
        block.block_data['nonce'] = hex(0)
        x = 0
        block.generate_hash(True)
        while not block.block_data['hash'].startswith('0' * Blockchain.difficulty):
            x += 1
            block.block_data['nonce'] = hex(x)
            block.generate_hash(False)
        return block
    def add_block(self, block: Block, proof: str) -> bool:
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of a latest block
          in the chain match.
        """
        if self.chain[-1].block_data['hash'] != block.block_data['previous_hash']:
            return False
        if self.check_proof(block, proof, True) == False:
            return False
        # block.hash = proof
        self.chain.append(block)
        Blockchain.index += 1
        return True
    def check_proof(self, block: Block, block_hash: str, force: bool) -> bool:
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.generate_hash(force))
    def dump_pool(self):
        with open('tx_pool.json', 'r') as pool:
            for transaction in pool:
                self.unconfirmed_transactions.append(transaction)
        open('tx_pool.json', 'w').close()
    def mine(self) -> tuple:
        new_block = Block(Blockchain.index, [],
                    datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), self.chain[-1].block_data['hash'], '0x')
        with open('tx_pool.json', 'r') as pool:
            for transaction in pool:
                new_block.add_transaction(transaction)
        new_block = self.proof_of_work(new_block)
        self.add_block(new_block, new_block.block_data['hash'])
        open('tx_pool.json', 'w').close()
        return (Blockchain.index, new_block)
    def check_chain_validity(self, start: int) -> bool:
        for i in range(start, len(self.chain)):
            block_hash = self.chain[i].block_data.get('hash')
            if check_proof(self.chain[i], block_hash, True) and \
                self.chain[i].block_data.get('previous_hash') == self.chain[i - 1].block_data.get('hash'):
                return True
            return False
