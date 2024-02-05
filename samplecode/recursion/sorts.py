# MCS 275 Spring 2024 Lecture 12
"Recursive comparison sorts"

def merge(L0,L1):
    """
    Take sorted lists `L0` and `L1` and
    returns a list with the same items as
    `L0+L1` but which is in increasing 
    order.
    """
    i0 = 0  # index of item in L0 we use next
    i1 = 0  # index of item in L1 we use next
    L = []
    n0 = len(L0)
    n1 = len(L1)
    while i0<n0 and i1<n1:
        # decide which of L0 and L1 to take from
        if L0[i0] <= L1[i1]:
            # take from L0
            L.append(L0[i0])
            # advance the pointer to the next item in L0
            i0 += 1
        else:
            # take from L1
            L.append(L1[i1])
            # advance the pointer to the next item in L1
            i1 += 1
    # one of the two loops below never runs
    # the other one handles any leftovers
    while i0<n0:
        L.append(L0[i0])
        i0 += 1
    while i1<n1:
        L.append(L1[i1])
        i1 += 1
    print("merge({},{}) returns {}".format(L0,L1,L))
    # L now contains everything from L0 and L1, and is sorted
    return L

def mergesort(L):
    """
    Return a list with the same items as `L`
    but which is in increasing order.
    """
    print("mergesort({})".format(L))
    if len(L)<=1:
        return L[:] # identical copy of L, new list
    middle = len(L)//2 # half length, rounding down
    L0 = mergesort(L[:middle]) # sorted first half
    L1 = mergesort(L[middle:]) # sorted second half
    return merge(L0,L1) # merge sorted lists
