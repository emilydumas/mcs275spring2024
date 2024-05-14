"""Robot motion simulation with simple text-based graphics"""
# MCS 275 Spring 2024 Emily Dumas
# Lectures 5-6

from plane import Vector2, Point2
import bots
import random

width = 60
height = 30

current_bots = []
# 5 static bots
for _ in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.Bot(position=P))
# 5 wandering bots (N,S,E,W)
for _ in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.WanderBot(position=P))
# 5 fast-wandering bots (N,S,E,W,NE,NW,SE,SW)
for _ in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.FastWanderBot(position=P))
# 5 self-destructing bots (20 steps before they're gone)
for _ in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.DestructBot(position=P, active_time=20))

# Diagonal patrol bot
current_bots.append(
    bots.PatrolBot(
        position=Point2(2, 2),
        direction=Vector2(1, 1),
        steps=20,
    )
)

# Horizontal patrol bot
current_bots.append(
    bots.PatrolBot(
        position=Point2(58, 5),
        direction=Vector2(-1, 0),
        steps=27,
    )
)

n = 0
while True:
    print("\n" * 3 * height)
    board = [[" "] * width for _ in range(height)]
    for b in current_bots:
        if not b.active:
            continue
        elif b.position.x < 0 or b.position.x >= width:
            continue
        elif b.position.y < 0 or b.position.y >= height:
            continue
        board[b.position.y][b.position.x] = "*"
    for row in board:
        print("".join(row))
    print("time={}".format(n))
    input()

    for b in current_bots:
        b.update()  # what type of object is b?  Doesn't matter
    n += 1
