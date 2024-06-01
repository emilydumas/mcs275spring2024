# MCS 275 Spring 2024 Project 3 Solution Stress Test
# Emily Dumas
"Make a big `BlockNode` tree"

from bstore import BlockNode


T = BlockNode()

a = 1664525
c = 1013904223

x = 1623
y = 8392

for n in range(5000):
    x = (a*x + c) % (2**32)
    y = (a*y + c) % (2**32)
    idx = x % (n+1)
    datum = y % 600
    print("Insert #{}: idx={} datum={}".format(n+1,idx,datum))
    T.insert(idx,datum)
    print(
        "Tree stats: size={} nodes={} depth={}".format(
            len(T),T.nodes(), T.depth()
        )
    )

