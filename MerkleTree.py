from hashlib import sha256
import json

class Node:
    def __init__(self, data: str):
        self.data = data
        try:
            self.sig = json.loads(data)['signature']
        except:
            self.sig = 'default'
        self.right = None
        self.left = None
        self.hash = ''
    def generate_hash(self):
        if self.right == None and self.left == None:
            self.hash = sha256(self.data.encode('utf-8')).hexdigest()
        elif self.right == None and self.left != None:
            self.hash = sha256(self.left.hash).hexdigest()
        elif self.right != None and self.left == None:
            self.hash = sha256(self.right.hash).hexdigest()
        else:
            self.hash = sha256(self.left.hash + self.right.hash).hexdigest()

class MerkleTree:
    def __init__(self, data: str):
        """
        A Merkle Tree is where the root is the resulting hash.
        The root hash is computed by computing the combined
        hash of its child nodes
                        head = hash (H1 + H2)
                                /   \
            (H1 = hash (children))   (H2 = hash (children))
        """
        self.root = Node(data)
        self.node_count = 1
        self.node_of_last_computed_hash = 0
    def insert(self, data: str) -> bool:
        '''
        Inserts based on transaction signature to avoid
        duplicate transactions
        '''
        pointer = self.root
        sig = json.loads(data)['signature']
        while pointer != None:
            if pointer.sig > sig:
                pointer = pointer.left
            elif pointer.sig < sig:
                pointer = pointer.right
            else:
                return False
        pointer = Node(data)
        self.node_count += 1
        return True
    def post_order(self, parent: Node):
        if parent == None:
            return
        self.post_order(parent.left)
        self.post_order(parent.right)
        parent.generate_hash()
    def compute_hash(self) -> str:
        #Saves computation time
        if (self.node_count == self.node_of_last_computed_hash):
            return self.root.hash
        #Use post-order traversal to compute hash
        self.post_order(self.root)
        self.node_of_last_computed_hash = self.node_count
        return self.root.hash
