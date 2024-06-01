# MCS 275 Spring 2024 Project 3 Solution
# Emily Dumas
"Demo and tests of the BlockNode class"

from bstore import BlockNode
import random
import time


def banner(msg):
    "Print `msg` with a bar above and below it"
    msg = " " + msg + " "
    bar = "=" * len(msg)
    print(bar)
    print(msg)
    print(bar)


banner("1. Report on small scale randomly added data")
T = BlockNode()

for n in range(20):
    T.insert(random.randrange(n + 1), random.randrange(10))
    print("\ndata={}".format(list(T)))
    print(
        "Tree stats: nodes={} depth={} root_data={}".format(
            T.nodes(), T.depth(), T.content[: T.size]
        )
    )

print()
banner("2. Correctness test")
N_CORRECT = 1000
T = BlockNode()
L = []
for n in range(N_CORRECT):
    x = random.randrange(1000)
    idx = random.randrange(n + 1)
    L.insert(idx, x)
    T.insert(idx, x)
    assert len(T) == n + 1, "After {} inserts, tree T reported length {}".format(
        n + 1, len(T)
    )
    # Check that they have identical items
    assert (
        list(T) == L
    ), "After {} identical inserts, tree T and list L report differing items".format(
        n + 1
    )
print("Correctness test with {} items: OK".format(n + 1))

print()
banner("3. Time test")
N_TIME_TEST = 100_000
data = [random.randrange(1000) for _ in range(N_TIME_TEST)]
indices = [random.randrange(i + 1) for i in range(N_TIME_TEST)]

L = []
t0 = time.time()
for i in range(N_TIME_TEST):
    L.insert(indices[i], data[i])

print("LIST insert time test: {:.2f} seconds".format(time.time() - t0))

T = BlockNode()
t0 = time.time()
for i in range(N_TIME_TEST):
    T.insert(indices[i], data[i])

print("TREE insert time test: {:.2f} seconds".format(time.time() - t0))
