# MCS 275 Spring 2024 Project 1 Starter Pack
"Simulation of factory and shipping logistics"

# Running this script is encouraged, but you
# don't need to read it or dissect how it works.

from fixtures import Crate, CrateQueue
import random  # used to select random line
import collections.abc  # used to check if something is a list

__version__ = "1.0"


def is_listlike(obj):
    "Is `obj` a non-string sequence?"
    return isinstance(obj, collections.abc.Sequence) and not isinstance(obj, str)


print("MCS 275 Spring 2024 Project 1 Simulator v" + __version__)
print("Preliminaries:")
print("\tImporting `routing.py`...", end="")
try:
    import routing

    print("OK")
except Exception as e:
    print("FAILED")
    raise

print("\tEnumerating available `Router` subclasses...", end="")
for name in ["Router", "OldRouter"]:
    if not name in dir(routing):
        print("FAILED")
        print("routing module does not contain class named `{}`".format(name))


def classdepth(cls):
    "Return length of the chain of parent classes of `cls`"
    if cls.__bases__:
        return 1 + classdepth(cls.__bases__[0])
    else:
        return 0


router_classes = []
for s in dir(routing):
    c = getattr(routing, s)
    try:
        if issubclass(c, routing.Router):
            router_classes.append(c)
    except TypeError:
        continue
router_classes.sort(key=lambda c: classdepth(c))
print("OK")


# Selection of routing class
router_cls = routing.OldRouter
while True:
    print()
    print("Available routing strategies:")
    for i, c in enumerate(router_classes):
        print("{:2d}. {}".format(i + 1, c.__name__))
    print(
        "Press Enter to use {}, or select a strategy by number:".format(
            router_cls.__name__
        )
    )
    s = input().strip()
    try:
        if s:
            k = int(s)
            if k < 1:
                raise IndexError("list index out of range")
            router_cls = router_classes[k - 1]
            print("OK, using {}".format(router_cls.__name__))
    except Exception as e:
        print("Invalid input: {}".format(e))
        continue
    break

# Selection of queue sizes
qlens = [3, 3, 2, 5, 4]
NQ = len(qlens)
while True:
    print()
    print("Queue lengths: Press Enter to use default {}".format(repr(qlens)))
    print("or enter comma-separated integer lengths:")
    s = input().strip()
    try:
        if s:
            fields = s.replace("[", "").replace("]", "").replace(",", " ").split()
            input_lens = [int(x) for x in fields]
            if len(input_lens) != NQ:
                raise ValueError("Expect {} integers".format(NQ))
            if min(input_lens) <= 0:
                raise ValueError("All lengths must be positive")
            qlens = input_lens
    except Exception as e:
        print("Invalid input: {}".format(e))
        continue
    break

# Preparation
print("Preparing simulation:")

print("\tMaking queues...", end="")
queues = [CrateQueue(maxlen=n) for n in qlens]
print("OK")

print("\tMaking router...", end="")
R = router_cls(input_queues=queues)
print("OK")

# Running the simulation:
mode = "update"
cratesymbols = "abcdefghijklmnopqrstuvwxyz"
cratesymbols += cratesymbols.upper()
cratesymbols += "!@#$%^&*-+=\\<>"
ns = len(cratesymbols)
cratecounts = [0 for _ in queues]
clear = "\n" * 40
status = "ready"
truck = []
half = NQ // 2
while True:
    k = 5
    cratelists = []
    for Q in queues:
        # Note: access to CrateQueue.items forbidden in routing.py!
        CL = ["-" for _ in range(Q.remaining_space())] + [
            "[{}]".format(c.label) for c in Q.items
        ]
        cratelists.append(CL)
        k = max(k, max([len(s) for s in CL]))
    crtfmt = "{:^" + str(k) + "s}"
    qstrs = [" ".join(crtfmt.format(s) for s in L) for L in cratelists]
    width = (k + 1) * max(qlens)
    rowfmt = "LINE {}-{}-> {:>" + str(width) + "} \u2502"
    print(clear)
    print("STATUS:", status)
    print("ROUTER:", R)
    x = width + 3
    print(
        "\u2500" * (x // 2)
        + "\u2524FACTORY\u251C"
        + "\u2500" * (x - x // 2)
        + "\u252C"
        + "\u2500" * 3
        + "\u2524SHIPPING DEPOT\u251C"
        + "\u2500" * 3
    )
    for i, s in enumerate(qstrs):
        print(rowfmt.format(i, "-" if queues[i].remaining_space() else "X", s), end="")
        if mode in ["arrived", "loaded"]:
            if i == half - 1:
                print(" \u2553" + "\u2500" * (3 * (k + 1) - 1) + "\u2556")
            elif i == half:
                truck_crate_strs = ["[{}]".format(c.label) for c in truck] + ["-"] * (
                    3 - len(truck)
                )
                print(
                    " \u2551"
                    + " ".join(crtfmt.format(s) for s in truck_crate_strs)
                    + "\u255F\u2500\u2510"
                )
            elif i == half + 1:
                print(
                    " \u2559"
                    + "\u2500o"
                    + "\u2500" * (3 * (k + 1) - 5)
                    + "o\u2500\u2568o\u2518"
                )
            else:
                print()
        else:
            print()

    print(
        "\u2500" * (width + 12) + "\u2534" + "\u2500" * 3 + "\u2500" * 16 + "\u2500" * 3
    )
    if mode == "update":
        print(
            "T = load truck | 0-{} = add to line | Enter = add random".format(
                len(qlens)
            )
        )
        s = input().lower()
        if s == "t":
            mode = "arrived"
            status = "truck at depot"
            continue
        if s == "":
            i = random.randint(0, NQ - 1)
        else:
            try:
                i = int(s)
                assert i >= 0
                assert i < NQ
            except Exception:
                status = "last command unrecognized; ready"
                continue
        Q = queues[i]
        if Q.is_full():
            status = "line {} cannot add to queue (full); ready".format(i)
        else:
            cr = Crate(label=str(i) + cratesymbols[cratecounts[i] % ns])
            Q.insert(cr)
            cratecounts[i] += 1
            if Q.is_full():
                status = "crate added at line {0}, line shut down; ready".format(i)
            else:
                status = "crate added at line {0}; ready".format(i)
    elif mode == "arrived":
        print("Press Enter to load the truck")
        input()
        B = R.prepare_load()
        assert is_listlike(B), "prepare_load did not return a list"
        for c in B:
            assert isinstance(
                c, Crate
            ), "list returned by prepare_load contained a non-Crate object"
        assert len(B) <= 3, "prepare_load returned list of length {} (too long)".format(
            len(B)
        )
        for c in B:
            truck.append(c)
        status = "truck loaded"
        mode = "loaded"
    elif mode == "loaded":
        print("Press Enter to dispatch truck")
        input()
        truck.clear()
        status = "truck dispatched; ready"
        mode = "update"
