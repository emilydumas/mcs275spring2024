# MCS 275 Spring 2024 Lectures 15-17
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
    """
    Binary search tree supporting search and insert, keys can be of any
    type supporting comparison.  Single node with key `None` represents
    an empty tree.
    """

    def search(self, k, verbose=False):
        """
        Find and return a node of this BST with key `k`, or return None
        if no such node exists
        """
        if verbose:
            print("search({}) called on {}".format(k, self))
        if self.key == None:
            if verbose:
                print("Empty tree does not contain {}".format(k))
            # empty tree; definitely does not contain k
            return None

        # Maybe the root has key k
        if k == self.key:
            return self
        # Otherwise, it's someone else's problem.  Whose?
        if k < self.key:
            # have the left subtree look for it...
            #   self.left might be another BST
            #   or it might be None, if there's no left child
            if self.left == None:
                # k would need to be in the left subtree
                # which does not exist.  Therefore k is not present
                return None
            else:
                if verbose:
                    print("{} < {}, descending into left subtree".format(k, self.key))
                return self.left.search(k, verbose=verbose)
        else:
            # have the right subtree look for it
            if self.right == None:
                return None
            else:
                if verbose:
                    print("{} > {}, descending into right subtree".format(k, self.key))
                return self.right.search(k, verbose=verbose)

    def insert(self, k):
        """
        Given key `k` that is not present in the BST with this node as
        its root, find a place where a node with that key can be added
        and add it.
        """
        if self.key == None:
            # tree is empty, this root node is waiting for a key
            self.key = k
            return

        if k == self.key:
            raise ValueError(
                "Duplicate keys are not allowed in this BST implementation"
            )

        # See MCS 275 2022 Project 3 solutions for for-loop way of doing this.

        if k < self.key:
            if self.left == None:
                # k belongs in the left subtree of this node,
                # which is empty.  Great!  Just add k as the
                # first node in the left subtree.
                node = BST(key=k)  # new node with key k
                self.set_left(node)  # attach it as the left child
            else:
                # k belong in the left subtree, which already has
                # stuff in it.  Ask it to handle k.
                return self.left.insert(k)
        else:
            if self.right == None:
                node = BST(key=k)  # new node with key k
                self.set_right(node)  # attach it as the right child
            else:
                return self.right.insert(k)
