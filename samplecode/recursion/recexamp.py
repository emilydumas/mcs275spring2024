# MCS 275 Spring 2024 Lectures 8 to 10
# Recursion examples
# David Dumas

call_counts = {"fib": 0}


def fac(n, verbose=False):
    "Return the factorial of a nonnegative integer n"
    # Optional: Show all function calls
    if verbose:
        print("fac({}) called".format(n))
    call_counts["fib"] += 1  # record this call
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
def fib(n, verbose=False):  # 1
    "nth Fibonacci number"
    # Optional: Show all function calls
    if verbose:
        print("fib({}) called".format(n))
    call_counts["fib"] += 1  # asks the global var call_count to change a value.
    # stop condition
    if n <= 1:
        # F_0=0 and F_1=1
        return n
    # recursive calls
    return fib(n - 1, verbose) + fib(
        n - 2, verbose
    )  # + (# calls for n-1) + (# calls for n-2)
    # NOTE: ^--------------------^--- two self-calls = SLOW


fib_cache = {
    0: 0,  # n=0 then F_n=0
    1: 1,  # n=1 then F_n=1
}  # dict with values of n as keys and F_n as values


def fib_clear_cache():
    "Clear the cache used by fib_memoized"
    fib_cache.clear()
    for n in range(2):
        fib_cache[n] = n


def fib_memoized(n, verbose=False):
    "nth Fibonacci number"
    # Optional: Show all function calls
    if verbose:
        print("fib_memoized({}) called".format(n))

    # Use stored result if available (provides stop condition)
    if n in fib_cache:  # recall membership testing for dict tests for KEYS
        return fib_cache[n]
    # Otherwise, resume the recursive approach.
    res = fib_memoized(n - 1, verbose) + fib_memoized(n - 2, verbose)
    fib_cache[n] = res  # store this result in the cache
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

        print("fac({:3d}): rec took {:.5f}s, iter took {:.5f}s".format(n, trec, titer))

    print("\n\n" + "-" * 72)
    print("FIBONACCI")
    prev_trec = 0
    for n in range(15, 36):
        t0 = time.time()
        y = fib(n)
        t1 = time.time()
        trec = t1 - t0  # amount of time it took to compute fac(n)

        fib_clear_cache()  # so each test of `n` is independent, clear cache
        t0 = time.time()
        y = fib_memoized(n)
        t1 = time.time()
        tmemo = t1 - t0  # amount of time it took to compute fac(n)

        t0 = time.time()
        y = fib_iterative(n)
        t1 = time.time()
        titer = t1 - t0  # amount of time it took to compute fac_iterative(n)

        # If the last value of `n` took at least 0.1 milliseconds, report the
        # percentage growth in trec for this iteration.
        if abs(prev_trec > 0.0001):
            incstr = " ({:+.1f}%)".format(100.0 * (trec - prev_trec) / (prev_trec))
        else:
            incstr = ""

        print(
            "fib({:3d}): rec {:.5f}s{}, memo {:.5f}s iter {:.5f}s".format(
                n,
                trec,
                incstr,
                tmemo,
                titer,
            )
        )
        prev_trec = trec

    print("\n\n" + "-" * 72)
    print("LARGE-n FIBONACCI")
    for n in range(0, 996, 100):
        fib_clear_cache()  # so each test of `n` is independent, clear cache
        t0 = time.time()
        y = fib_memoized(n)
        t1 = time.time()
        tmemo = t1 - t0  # amount of time it took to compute fac(n)

        t0 = time.time()
        y = fib_iterative(n)
        t1 = time.time()
        titer = t1 - t0  # amount of time it took to compute fac_iterative(n)

        print(
            "fib({:3d}): memo {:.5f}s iter {:.5f}s".format(
                n,
                tmemo,
                titer,
            )
        )

    print("\n\n" + "-" * 72)
    print("fib call counts")
    print("{:2s} {:6s}".format("n", "calls"))
    for n in range(15):
        call_counts["fib"] = 0
        y = fib(n)
        print("{:2d} {:5d}".format(n, call_counts["fib"]))


if __name__ == "__main__":  # means "if run as a script"
    import time

    # do timing tests and print the results
    timing_study()

# but when imported as a module, only process function definitions
