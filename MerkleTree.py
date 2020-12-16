from hashlib import sha256

class MerkleTree:
    def __init__(self, data: str):
        """
        A Merkle Tree is where the root is the resulting hash
        The root hash is computed by computing the combined
        hash of its child nodes
                        head = hash (H1 + H2)
                                /   \
            (H1 = hash (children))   (H2 = hash (children))
        """
        self.root = Node(data)
    def insert(self, data: str):
        pointer = self.root
        while pointer != None:
            if pointer.data > data:
                pointer = pointer.left
            elif pointer.data <= data:
                pointer = pointer.right
            else:
                pass
        pointer = Node(data)
    def compute_hash(self) -> str:
        #Use post-order traversal to compute hash
        post_order(self.root)
        return self.root.hash
    def post_order(self, parent: Node):
        if root == None:
            return
        post_order(parent.left)
        post_order(parent.right)
        parent.generate_hash()

class Node:
    def __init__(self, data: str):
        self.data = data
        self.right = None
        self.left = None
        self.hash = ''
    def generate_hash(self):
        if self.right == None and self.left == None:
            self.hash = sha256(self.data).hexdigest()
        else:
            self.hash = sha256(self.left.hash + self.right.hash).hexdigest()
