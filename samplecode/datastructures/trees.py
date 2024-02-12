# MCS 275 Spring 2024 Lecture 15
# David Dumas
"Classes for tree-like data structures"

class Node:
    "Node in a binary tree, or the entire tree below this node"
    def __init__(self,key=None):
        "Creates a node with no children"
        self.left = None
        self.right = None
        self.parent = None
        self.key = key

    def set_left(self,n):
        "Make `Node` object `n` the left child of this node"
        self.left = n   # n is our child
        n.parent = self # ...and tell n that we are its parent

    def set_right(self,n):
        "Make `Node` object `n` the right child of this node"
        self.right = n   # n is our child
        n.parent = self # ...and tell n that we are its parent

    def __str__(self):
        "human-readable string representation"
        return "<{}>".format(self.key)

    def __repr__(self):
        "unambiguous developer-friendly representation"
        return str(self)