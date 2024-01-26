# MCS 275 Spring 2024 Lecture 8
# Recursion examples
# David Dumas


def fac(n, verbose=False):
    "Return the factorial of a nonnegative integer n"
    # Optional: Show all function calls
    if verbose:
        print("fac({}) called".format(n))
    # Optional: Check for invalid n
    if n < 0:
        raise ValueError("Factorial requires nonnegative argument")
    # stop condition
    if n <= 1:
        # 0! = 1 and 1! = 1
        return 1
    # recursive call
    return n * fac(n - 1, verbose)


# WARNING: For large n, this is ridiculously inefficient.
# More discussion in lecture 9.
def fib(n, verbose=False):
    "nth Fibonacci number"
    # Optional: Show all function calls
    if verbose:
        print("fib({}) called".format(n))
    # stop condition
    if n <= 1:
        # F_0=0 and F_1=1
        return n
    # recursive calls
    return fib(n - 1, verbose) + fib(n - 2, verbose)
    # NOTE: ^--------------------^--- two self-calls = SLOW


# Paper-folding sequence
# ----------------------

# For each nonnegative integer n, PFS(n) is a sequence of binary
# digits, e.g. PFS(2) is 1101100
# We represent such binary sequences as lists of integers, e.g.
# PFS(2) will return [1,1,0,1,1,0,0]

# Key observation
# PFS(n) = PFS(n-1), then 1, then reverse-order 0/1-flipped PFS(n-1)


def PFS(n):
    """
    Compute the nth paper folding sequence, where n
    is a nonnegative integer.
    """
    if n == 0:
        return []  # no creases in a unfolded piece of paper!
    L = PFS(n - 1)
    return L + [1] + [1 - x for x in L[::-1]]
    #                   ^-- flip         ^-- reverse
