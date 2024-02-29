# MCS 275 Spring 2024 Lectures 15-17 and Worksheets 7-8
# David Dumas
"Classes representing tree-like data structures"

import json


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

    def inorder(self):
        "Return a list of all nodes visited by an inorder traversal"
        # inorder = left, node, right
        left = []
        right = []
        if self.left:
            left = self.left.inorder()
        if self.right:
            right = self.right.inorder()
        return left + [self] + right

    def preorder(self):
        "Return a list of all nodes visited by an preorder traversal"
        left = []
        right = []
        if self.left:
            left = self.left.preorder()
        if self.right:
            right = self.right.preorder()
        return [self] + left + right

    def postorder(self):
        "Return a list of all nodes visited by a postorder traversal"
        left = []
        right = []
        if self.left:
            left = self.left.postorder()
        if self.right:
            right = self.right.postorder()
        return left + right + [self]

    # Part of solution to Worksheet 8 problem 1
    # (adapted from older course materials prepared by
    #  TAs Johnny Joyce and Kylash Viswanathan)
    def as_dict_tree(self):
        """
        Returns representation of the nodes in the tree
        as a collection of nested dictionaries.
        """

        # Initialize left and right keys as None so they can be overwritten if needed
        D = {"key": self.key, "left": None, "right": None}

        if self.left != None:
            D["left"] = self.left.as_dict_tree()

        if self.right != None:
            D["right"] = self.right.as_dict_tree()

        return D

    # Part of solution to Worksheet 8 problem 1
    # (adapted from older course materials prepared by
    #  TAs Johnny Joyce and Kylash Viswanathan)
    def save(self, fp):
        """
        Make a JSON representation of the tree and write it to
        the already-open file object `fp`.
        """
        tree = self.as_dict_tree()
        json.dump({"class": self.__class__.__name__, "tree": tree}, fp)


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
            print("search({}) called with root node {}".format(k, self))
        if self.key == None:
            # the tree is empty, so in particular `k` is not there
            return None
        # Maybe the root has key k
        if k == self.key:
            return self
        # Otherwise, it's someone else's problem.  Whose?
        if k < self.key:
            if verbose:
                print("{} < {}, so descend into left subtree".format(k, self.key))
            # have the left subtree look for it...
            #   self.left might be another BST
            #   or it might be None, if there's no left child
            if self.left == None:
                # k would need to be in the left subtree
                # which does not exist.  Therefore k is not present
                if verbose:
                    print("Left subtree empty; {} not present".format(k))
                return None
            else:
                return self.left.search(k, verbose=verbose)
        else:
            if verbose:
                print("{} > {}, so descend into right subtree".format(k, self.key))
            # have the right subtree look for it
            if self.right == None:
                if verbose:
                    print("Right subtree empty; {} not present".format(k))
                return None
            else:
                return self.right.search(k, verbose=verbose)

    def insert(self, k, verbose=False):
        """
        Given a key `k` that is not present in the BST, find a suitable
        place and add a new node to the BST with key `k`
        """
        if verbose:
            print("insert({}) called with root node {}".format(k, self))
        if self.key == None:
            # the tree is empty, so k can become the key of this node
            if verbose:
                print("Tree is empty, setting root key to {}".format(k))
            self.key = k
            return

        if k == self.key:
            raise ValueError("Duplicate keys are not allowed in BST")

        if k < self.key:
            # Any node with key `k` would need to go
            # in the left subtree.
            if verbose:
                print(
                    "{0} < {1}, therefore {0} must go in the left subtree".format(
                        k, self.key
                    )
                )

            if self.left == None:
                # There's no left subtree, so `k` can be the first key there.
                if verbose:
                    print(
                        "Left subtree empty.  Adding a node with key {} as left child.".format(
                            k
                        )
                    )
                node = BST(key=k)  # new node
                self.set_left(node)  # make the new node our left child
            else:
                if verbose:
                    print(
                        "{0} < {1} and there is a left child; descend into left subtree".format(
                            k, self.key
                        )
                    )

                return self.left.insert(k, verbose=verbose)
        else:
            if verbose:
                print(
                    "{0} > {1}, therefore {0} must go in the right subtree".format(
                        k, self.key
                    )
                )
            if self.right == None:
                if verbose:
                    print(
                        "Right subtree empty.  Adding a node with key {} as right child.".format(
                            k
                        )
                    )
                # There's no right subtree, so `k` can be the first key there.
                node = BST(key=k)  # new node
                self.set_right(node)  # make the new node our right child
            else:
                if verbose:
                    print(
                        "{0} > {1} and there is a right child; descend into right subtree".format(
                            k, self.key
                        )
                    )
                return self.right.insert(k, verbose=verbose)

    # From Worksheet 7 Solutions
    def minimum(self):
        """
        In the subtree that this node is the root of, find and
        return the the smallest key.
        """
        if self.left != None:
            return self.left.minimum()
        else:
            return self.key

    # From Worksheet 7 Solutions
    def maximum(self):
        """
        In the subtree that this node is the root of, find and
        return the the largest key.
        """
        if self.right != None:
            return self.right.maximum()
        else:
            return self.key


# Part of solution to Worksheet 8 problem 1
# (adapted from older course materials prepared by
#  TAs Johnny Joyce and Kylash Viswanathan)
def dict_tree_to_nodes(D, node_type):
    """
    Converts a nested dict to binary tree using `node_type`
    as the node class (should be `Node` or `BST`).
    """
    N = node_type(D["key"])

    if D["left"] != None:  # Recursive call on left side if needed
        N.set_left(dict_tree_to_nodes(D["left"], node_type))

    if D["right"] != None:  # Recursive call on right side if needed
        N.set_right(dict_tree_to_nodes(D["right"], node_type))

    return N


# Part of solution to Worksheet 8 problem 1
# (adapted from older course materials prepared by
#  TAs Johnny Joyce and Kylash Viswanathan)
def load(fp):
    """
    Loads a tree from a JSON object read from `fp`
    (which should be a file object open for reading)
    """
    T = json.load(fp)
    node_type = {"Node": Node, "BST": BST}[T["class"]]
    return dict_tree_to_nodes(T["tree"], node_type)
