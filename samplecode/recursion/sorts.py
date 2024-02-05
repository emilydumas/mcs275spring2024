# MCS 275 Spring 2024 Lecture 12
"Recursive comparison sorting examples"

def merge(L0,L1):
    """
    Takes sorted lists L0 and L1 and returns a list containing
    the same elements as L0+L1, but which is sorted
    """
    L = [] # destination for elements as we examine them
    n0 = len(L0)
    n1 = len(L1)
    i0 = 0 # where we are in L0
    i1 = 0 # where we are in L1

    while i0<n0 and i1<n1:
        if L0[i0] <= L1[i1]:
            L.append(L0[i0]) # take the item from L0
            i0 += 1 # go to next item in L0
        else:
            L.append(L1[i1]) # take the item from L1
            i1 += 1 # go to next item in L1
    # Handle unused elements from L0, if any
    while i0<n0:
        L.append(L0[i0])
        i0 += 1
    # Handle unused elements from L1, if any
    while i1<n1:
        L.append(L1[i1])
        i1 += 1
    print("merge({},{}) returns {}".format(L0,L1,L))
    return L # L is now sorted and has all elements in L0 or L1

        
        

    

def mergesort(L):
    """
    Take a list of comparable objects `L`
    and return a list with the same items in
    increasing order
    """
    print("mergesort({})".format(L))
    # stop condition
    if len(L)<=1:
        return L[:]  # This means "a copy of L"
    # split
    middle = len(L)//2  # half length, rounding down
    L0 = L[:middle]
    L1 = L[middle:]
    # recursion
    L0sorted = mergesort(L0)
    L1sorted = mergesort(L1)
    # merge
    return merge(L0sorted,L1sorted)  # merge two sorted lists