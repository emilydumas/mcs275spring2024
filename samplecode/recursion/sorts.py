# MCS 275 Spring 2024 Lecture 12
"Recursive comparison sorting examples"


def merge(L0, L1, verbose=False):
    """
    Takes sorted lists L0 and L1 and returns a list containing
    the same elements as L0+L1, but which is sorted
    """
    L = []  # destination for elements as we examine them
    n0 = len(L0)
    n1 = len(L1)
    i0 = 0  # where we are in L0
    i1 = 0  # where we are in L1

    while i0 < n0 and i1 < n1:
        if L0[i0] <= L1[i1]:
            L.append(L0[i0])  # take the item from L0
            i0 += 1  # go to next item in L0
        else:
            L.append(L1[i1])  # take the item from L1
            i1 += 1  # go to next item in L1
    # Handle unused elements from L0, if any
    while i0 < n0:
        L.append(L0[i0])
        i0 += 1
    # Handle unused elements from L1, if any
    while i1 < n1:
        L.append(L1[i1])
        i1 += 1
    if verbose:
        print("merge({},{}) returns {}".format(L0, L1, L))
    # L now contains everything from L0 and L1, and is sorted
    return L


def mergesort(L, verbose=False):
    """
    Return a list with the same items as `L`
    but which is in increasing order.
    """
    if verbose:
        print("mergesort({})".format(L))
    if len(L) <= 1:
        return L[:]  # identical copy of L, new list
    middle = len(L) // 2  # half length, rounding down
    L0 = mergesort(L[:middle], verbose=verbose)  # sorted first half
    L1 = mergesort(L[middle:], verbose=verbose)  # sorted second half
    return merge(L0, L1, verbose=verbose)  # merge sorted lists


def demo():
    "Demonstrate the sorting functions above"

    # Demo merge on two sorted halves of 1..9
    L = list(range(1, 10))
    random.shuffle(L)
    L0 = L[:5]
    L1 = L[5:]
    L0.sort()
    L1.sort()
    print("Verbose merge({},{}):".format(L0, L1))
    assert merge(L0, L1, verbose=True) == list(range(1, 10))
    print()

    # Demo mergesort on random order of 1..9
    L = list(range(1, 10))
    random.shuffle(L)
    print("Verbose sort of {}".format(L))
    assert mergesort(L, verbose=True) == list(range(1, 10))
    print()

    # Test mergesort on 10,000 random shuffles of 0..99
    print(
        "Testing mergesort 10,000 times...",
        end="",
        flush=True,
    )
    for _ in range(10_000):
        L = list(range(100))
        random.shuffle(L)
        assert mergesort(L) == list(range(100))
    print("OK")


if __name__ == "__main__":
    import random

    demo()
