from Block import Block
from datetime import datetime

class Blockchain:
    difficulty = 3
    index = 0
    def __init__(self):
        self.genesis_block = Block(0, '__GENESIS__', datetime.now(), '0')
        self.genesis_block.generate_hash()
        self.chain = [self.genesis_block]
        self.unconfirmed_transactions = []
        Blockchain.index += 1
    def proof_of_work(self, block: Block) -> Block:
        block.nonce = hex(0)
        x = 0
        block.generate_hash()
        while not block.hash.startswith('0' * Blockchain.difficulty):
            x += 1
            block.nonce = hex(x)
            block.generate_hash()
        return block
    def add_block(self, block: Block, proof: str) -> bool:
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of a latest block
          in the chain match.
        """
        if self.chain[-1].hash != block.previous_hash:
            return False
        if self.check_proof(block, proof) == False:
            return False
        # block.hash = proof
        self.chain.append(block)
        Blockchain.index += 1
        return True
    def check_proof(self, block: Block, block_hash: str) -> bool:
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.generate_hash())
    def load_unconfirmed_transaction(self):
        with open('tx_pool.json', 'r') as pool:
            for transaction in pool:
                self.unconfirmed_transactions.append(transaction)
        open('tx_pool.json', 'w').close()
    def mine(self) -> int:
        new_block = Block(Blockchain.index, self.unconfirmed_transactions,
                    datetime.now(), self.chain[-1].hash)
        new_block = self.proof_of_work(new_block)
        self.add_block(new_block, new_block.hash)
        self.unconfirmed_transactions = []
        return Blockchain.index - 1
