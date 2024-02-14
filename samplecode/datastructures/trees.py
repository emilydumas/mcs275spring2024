# MCS 275 Spring 2024 Lecture 15
# David Dumas
"Classes representing tree-like data structures"


class Node:
    "Node in a binary tree, or the binary tree itself"

    def __init__(self, key=None):
        "Make a new node with no children"
        self.parent = None
        self.left = None
        self.right = None
        self.key = key

    def set_left(self, n):
        "Make `Node` object `n` the left child of this one"
        self.left = n  # record that we have a left child
        n.parent = self  # ...and that we are now the parent of n

    def set_right(self, n):
        "Make `Node` object `n` the right child of this one"
        self.right = n  # record that we have a right child
        n.parent = self  # ...and that we are now the parent of n

    def __str__(self):
        "Human-readable string representing this object"
        return "<{}>".format(self.key)

    def __repr__(self):
        "Unambiguous string representing this object, intended for developers"
        return str(self)

class BST(Node):
    "Binary search tree supporting search by key and node insertion"
    def search(self,k):
        "Find and return a node with key `k`, or None if no such node exists"
        if k == self.key:
            # This node is the right one, return it
            return self
        # k is not the key of self, so if k is present it's in the left or right subtree

        if k < self.key:
            if self.left != None:
                # the left subtree exists, so search it
                return self.left.search(k)
            else:
                # k would need to be in the left subtree
                # but there's no left subtree!
                return None # not found
        else:
            if self.right != None:
                return self.right.search(k)
            else:
                return None
            
    def insert(self,k):
        """
        Create a node with key `k` and add it to the tree, preserving the BST property
        Requires that key `k` is not present in the tree already!
        """
        
