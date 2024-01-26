# MCS 275 Spring 2024 Lecture 8
# Recursion examples
# David Dumas

# n! = n * (n-1)!
# 0! = 1 (empty product)
# 1! = 1 (product of just 1)
def fac(n):
    "Compute the factorial of a nonnegative integer `n`"
    # stop condition
    if n <= 1:
        # 0! = 1! = 1
        return 1
    # recursive call (and return)
    return n * fac(n-1)

# fib(0) = 0 = F_0
# fib(1) = 1 = F_1
# So (by accident) fib(n)=n if n <= 1

# WARNING: Ridiculously inefficient recursive implementation
def fib(n):
    "nth Fibonacci number"
    # TODO: stop condition
    if n<=1:
        # F_n=n if n<=1
        return n
    # recursive call
    return fib(n-1) + fib(n-2) # <--- TODO: Discuss problem with this.


#[1,1,0]
#[1,1,0,1,1,0,0]
#[1,1,0,1,1,0,0,   1,    1,1,0,0,1,0,0]
#                       ^^^^^^^^^^^^^^  ---> reverse ->  0,0,1,0,0,1,1  
#                                       ----> flip 0/1 ->1,1,0,1,1,0,0  PFS(n-1)!!
# First obs: PFS(n) seems to start
# with PFS(n-1)

# PFS(n) is the same as:
# PFS(n-1), then a 1, then PFS(n-1) reversed (opposite order) and flipped (0<->1)

def PFS(n):
    "Return the nth paper folding sequence (a list of integers)"
    # stop condition
    if n==0:
        return []
    # recursive call
    L = PFS(n-1)
    return L + [1] + [ 1-x for x in L[::-1] ]
    #                  ^^^-flip 0/1     ^^- reverse
