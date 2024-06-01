# MCS 275 Spring 2024 Project 3 Solution
# Emily Dumas
"Module allowing one to store a sequence as a tree of blocks"


class BlockNode:
    """
    Data structure with list-like interface, supporting
    indexing and insert at any position, backed by a
    tree of fixed-size blocks
    """

    MAX_CONTENT = 6  # size of block (must be even)
    HALF_CONTENT = 3  # size of half block

    def __init__(self, initial_content=None, left_size=0):
        """
        Initialize a new node, either empty or with
        the items from `initial_content` if given.
        """
        self.left_size = left_size  # data items in left subtree
        self.content = [0 for _ in range(self.MAX_CONTENT)]
        # Optional assert to codify the requirement `initial_content`
        # cannot be too long
        assert (initial_content is None) or (len(initial_content) <= self.MAX_CONTENT)
        if initial_content is not None:
            self.size = len(initial_content)
            self.content[: self.size] = initial_content
        else:
            self.size = 0
        self.left = None
        self.right = None
        self.parent = None

    # THIS METHOD WAS NOT REQUIRED!
    def __str__(self):
        """
        String representation of the entire tree.
        Totally optional but helps debugging.
        """
        L = []
        for i, x in enumerate(self.content):
            if i < self.size:
                L.append(str(x))
            else:
                L.append("-")
        cs = "[{}]".format(",".join(L))
        s = "<ls={},content={}>".format(self.left_size, cs)
        if (self.left is None) and (self.right is None):
            return s
        else:
            return "{}\n  L:{}\n  R:{}".format(
                s,
                str(self.left).replace("\n", "\n    "),
                str(self.right).replace("\n", "\n    "),
            )

    # THIS METHOD WAS NOT REQUIRED!
    def __repr__(self):
        "Defer to __str__"
        return str(self)

    def depth(self):
        "Depth of the tree measured in edges"
        left_depth = 0
        right_depth = 0
        if self.left is not None:
            left_depth = 1 + self.left.depth()
        if self.right is not None:
            right_depth = 1 + self.right.depth()
        return max(left_depth, right_depth)

    def set_left(self, block):
        """
        Make `block` the left child of this one,
        also handling parent if `block` is not None
        """
        self.left = block
        if block is not None:
            block.parent = self

    def set_right(self, block):
        """
        Make `block` the right child of this one,
        also handling parent if `block` is not None
        """
        self.right = block
        if block is not None:
            block.parent = self

    def is_full(self):
        "Is every slot in this block occupied?"
        return self.size == self.MAX_CONTENT

    def split(self):
        """
        Replace this node with two or more nodes so that every
        item previously in this node is now in a non-full node.
        Should only be called when this node is full.
        """
        if self.left is None:
            # No left child, so add a new one there
            #   @@                   @
            #     \    becomes      / \
            #      R               @   R
            self._simple_left_split()
        elif self.right is None:
            # No right child, so add a new one there
            #   @@                   @
            #  /       becomes      / \
            # L                    L   @
            self._simple_right_split()
        else:
            # Both children exist, do this:
            #   @@                    O
            #  /  \     becomes      / \
            # L    R                @   @
            #                      /     \
            #                     L       R
            # where 'O' means an empty node
            self._complex_split()

    # I put underscores as first letter of any method that is
    # only meant for "internal" use (ie in other methods)
    def _simple_left_split(self):
        "Split this node, new one becomes left child"
        # New node that gets the first half of our data
        newblock = BlockNode(
            initial_content=self.content[: self.HALF_CONTENT],
            left_size=self.left_size,
        )
        newblock.set_left(self.left)
        self.set_left(newblock)
        # Move the scond half of our data to the beginning
        self.content[: self.HALF_CONTENT] = self.content[self.HALF_CONTENT :]
        # Adjust our size
        self.size = self.HALF_CONTENT
        # Record that HALF_CONTENT items added to left subtree
        self.left_size += self.HALF_CONTENT

    def _simple_right_split(self):
        "Split this node, new one becomes right child"
        # New node that gets the last half of our data
        newblock = BlockNode(
            initial_content=self.content[self.HALF_CONTENT :],
            left_size=0,
        )
        newblock.set_right(self.right)
        self.set_right(newblock)
        # Just decreasing our size effectively discards
        # the second half of our data, which is now stored
        # in the new right child.
        self.size = self.HALF_CONTENT

    def _complex_split(self):
        "Empty this node, moving its data to two new children"
        L_newblock = BlockNode(
            initial_content=self.content[: self.HALF_CONTENT],
            left_size=self.left_size,
        )
        R_newblock = BlockNode(
            initial_content=self.content[self.HALF_CONTENT :],
            left_size=0,
        )
        # HALF_CONTENT items added to left subtree
        self.left_size += self.HALF_CONTENT
        L_newblock.set_left(self.left)
        self.set_left(L_newblock)
        R_newblock.set_right(self.right)
        self.set_right(R_newblock)
        # Our data has been moved to our children
        # so we're empty now
        self.size = 0

    def insert(self, index, x):
        """
        Add a new item `x` whose data index is `index`, moving
        items at higher data indices to accommodate it.
        """

        # PREPARATION STEP
        # This node might be full.  That might not be a problem.
        # But if `x` is supposed to go in this node, or to
        # immediately follow it, then it complicates the process
        # of inserting it.  In either of those cases, we do some
        # surgery on the tree before proceeding.
        if self.is_full() and (self.left_size <= index <= self.left_size + self.size):
            self.split()  # See this method for details on what it does

        # The tree may have been changed by the `split()`` call above,
        # so we need to re-examine things like left_size, size,
        # and how they related to `index`.

        # But the call to `split()` ensures something important:
        # If `x` belongs in this block, then this block is NOT
        # FULL.

        if self.left_size <= index <= self.left_size + self.size:
            # `x` belongs in this block
            # Record the guarantee of the split process
            assert self.size < self.MAX_CONTENT
            # What content index?
            i = index - self.left_size
            # Make a spot for it
            if i < self.size:
                # There are items to move over to the right
                self.content[i + 1 : self.size + 1] = self.content[i : self.size]
            # Put `x` in the spot we made
            self.content[i] = x
            self.size += 1
        elif index < self.left_size:
            # `x` belongs in the left subtree
            if self.left is None:
                # Can only happen with negative index!
                raise IndexError("Invalid index: Too small")
            # Recursively call `insert` on the left subtree to
            # handle it.
            self.left.insert(index, x)
            # We now know that one thing ended up in our left
            # subtree; record that in `left_size`.
            self.left_size += 1
        else:
            if self.right is None:
                # Can only happen if index exceeds length
                raise IndexError("Invalid index: Too large")
            # Recursively call `insert` on the left subtree to
            # handle it.  Note we subtract `self.left_size+self.size`
            # because there are exactly that many data items in this
            # tree that are not "seen" when our left child is
            # taken as the root of a subtree.
            self.right.insert(index - (self.left_size + self.size), x)

    def __getitem__(self, index):
        "Retrieve an item by data index"
        if self.left_size <= index < self.left_size + self.size:
            # It's here
            return self.content[index - self.left_size]
        elif index < self.left_size:
            # It's in our left subtree
            if self.left is None:
                # Oops, there is no such thing; means index was bad
                raise IndexError("Invalid index: Too small")
            return self.left[index]
        else:
            # It's in our right subtree
            if self.right is None:
                # Oops, there is no such thing; means index was bad
                raise IndexError("Invalid index: Too large")
            return self.right[index - (self.left_size + self.size)]

    def __len__(self):
        "Number of data items in the entire tree"
        # Three contributors:
        # Items here (self.size)
        # Items in left subtree (self.left_size)
        # Items in right subtree (dunno, call `__len__` to count 'em)
        n = self.left_size + self.size
        if self.right is not None:
            n += len(self.right)
        return n

    def nodes(self):
        "Total number of nodes in this tree"
        return (
            1
            + (self.left.nodes() if self.left is not None else 0)
            + (self.right.nodes() if self.right is not None else 0)
        )

    def append(self, x):
        "Add an item after the last index currently used"
        self.insert(len(self), x)
