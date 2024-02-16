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
