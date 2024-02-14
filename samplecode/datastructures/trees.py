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
    "Binary search tree supporting search and insert"
    def search(self,k):
        """
        Find and return a node of this BST with key `k`, or return None
        if no such node exists
        """
        # Maybe the root has key k
        if k == self.key:
            return self
        # Otherwise, it's someone else's problem.  Whose?
        if k < self.key:
            # have the left subtree look for it
            #self.left might be another BST
            #but it might be None, if there's no left child
            if self.left == None:
                # k would need to be in the left subtree
                # which does not exist.  Therefore k is not present
                return None
            else:
                return self.left.search(k)
        else:
            # have the right subtree look for it
            if self.right == None:
                return None
            else:
                return self.right.search(k)
            


    def insert(self,k):
        """
        Find and return a node of this BST with key `k`, or return None
        if no such node exists
        """
        raise NotImplementedError