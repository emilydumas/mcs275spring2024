# MCS 275 Spring 2024 Lectures 8 and 9
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


def fac_iterative(n):
    "Compute the factorial of n without recursion"
    prod = 1  # product so far (STATE)
    for i in range(2, n + 1):  # i starts at 1, ends at n
        prod *= i
    return prod


# WARNING: For large n, this is ridiculously inefficient.
# The more efficient recursive method is memoization (below).
def fib(n, verbose=False):   # 1
    "nth Fibonacci number"
    # Optional: Show all function calls
    if verbose:
        print("fib({}) called".format(n))
    # stop condition
    if n <= 1:
        # F_0=0 and F_1=1
        return n
    # recursive calls
    return fib(n - 1, verbose) + fib(n - 2, verbose)  # + (# calls for n-1) + (# calls for n-2)
    # NOTE: ^--------------------^--- two self-calls = SLOW

fib_cache = {
    0:0,  # n=0 then F_n=0
    1:1,  # n=1 then F_n=1
}  # dict with values of n as keys and F_n as values

def fib_memoized(n, verbose=False):
    "nth Fibonacci number"
    # Optional: Show all function calls
    if verbose:
        print("fib({}) called".format(n))

    # Check to see if this value is already in the cache
    # If so, return it.  This includes the stop condition for n=0,1
    if n in fib_cache:  # reminder: in for dict means "is a key of"
        return fib_cache[n] # we know F_n, return it without computation

    # recursive calls
    res = fib_memoized(n - 1, verbose) + fib_memoized(n - 2, verbose)
    # Store the fact that `fib(n)`` returns `res` in the cache
    fib_cache[n] = res
    return res

def fib_iterative(n):
    if n == 0:
        return 0
    a = 0  # F_0
    b = 1  # F_1
    for _ in range(n - 1):
        a, b = b, a + b  # replaces F_(i-1), F_i with F_i, F_(i+1)
    return b


# An alternative to the approach above: Compute one extra term
# of the series and avoid the initial if statement.
#
# def fib_iterative(n):
#    "Iterative computation of nth term in Fibonacci sequence"
#    # a,b will be the last two Fib terms we know
#    a = 0  #F_0
#    b = 1  #F_1
#    for i in range(n):
#        a, b = b, a+b
#    return a


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


def timing_study():
    "Print timing tables for factorial and fibonacci"
    print("-" * 72)
    print("FACTORIAL")
    for n in range(0, 995, 50):
        t0 = time.time()
        y = fac(n)
        t1 = time.time()
        trec = t1 - t0  # amount of time it took to compute fac(n)

        t0 = time.time()
        y = fac_iterative(n)
        t1 = time.time()
        titer = t1 - t0  # amount of time it took to compute fac_iterative(n)

        print("fac({:3d}): rec took {:.4f}s, iter took {:.4f}s".format(n, trec, titer))

    print("\n\n" + "-" * 72)
    print("FIBONACCI")
    for n in range(35):
        t0 = time.time()
        y = fib(n)
        t1 = time.time()
        trec = t1 - t0  # amount of time it took to compute fac(n)

        t0 = time.time()
        fib_cache.clear()
        fib_cache[0]=0
        fib_cache[1]=1
        y = fib_memoized(n)
        t1 = time.time()
        tmemo = t1 - t0  # amount of time it took to compute fac(n)

        t0 = time.time()
        y = fib_iterative(n)
        t1 = time.time()
        titer = t1 - t0  # amount of time it took to compute fac_iterative(n)

        print("fib({:3d}): rec {:.5f}s, memo {:.5f}s iter {:.5f}s".format(
            n,
            trec,
            tmemo,
            titer,
        ))

    print("\n\n" + "-" * 72)
    print("LARGE-n FIBONACCI")
    for n in range(0,995,5):
        t0 = time.time()
        fib_cache.clear()
        fib_cache[0]=0
        fib_cache[1]=1
        y = fib_memoized(n)
        t1 = time.time()
        tmemo = t1 - t0  # amount of time it took to compute fac(n)

        t0 = time.time()
        y = fib_iterative(n)
        t1 = time.time()
        titer = t1 - t0  # amount of time it took to compute fac_iterative(n)

        print("fib({:3d}): memo {:.5f}s iter {:.5f}s".format(
            n,
            tmemo,
            titer,
        ))


if __name__ == "__main__":  # means "if run as a script"
    import time

    # do timing tests and print the results
    timing_study()

# but when imported as a module, only process function definitions
