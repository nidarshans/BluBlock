from hashlib import sha256

class MerkleTree:
    def __init__(self):
        """
        A Merkle Tree is where the root is the resulting hash
        The root hash is computed by computing the combined
        hash of its child nodes
                        head = hash (H1 + H2)
                                /   \
            (H1 = hash (children))   (H2 = hash (children))
        """
        self.root = Node(None)

class Node:
    def __init__(self, data: str):
        self.data = data
        self.right = None
        self.left = None
        self.hash = ''
    def generate_hash(self):
        self.hash = sha256(self.data).hexdigest()
