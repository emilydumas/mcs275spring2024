"""Robot motion simulation with unicode text graphics"""
# MCS 275 Spring 2024 David Dumas

# Bots are shown as characters.  For any Bot class that has an
# attribute `symbol`, the value of that attribute is used as the
# representing character.  Bot classes lacking this attribute are
# given numbers instead (in the order encountered), starting with 1.

from plane import Vector2, Point2
import bots
import random
import time

width = 60
height = 30

current_bots = []
for _ in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.Bot(position=P))
for _ in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.WanderBot(position=P))
for _ in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.DestructBot(position=P, active_time=20))
for _ in range(5):
    P = Point2(random.randint(0, width - 1), random.randint(0, height - 1))
    current_bots.append(bots.FastWanderBot(position=P))

current_bots.append(
    bots.PatrolBot(
        position=Point2(2, 2),
        direction=Vector2(1, 1),
        steps=20,
    )
)

current_bots.append(
    bots.PatrolBot(
        position=Point2(58, 5),
        direction=Vector2(-1, 0),
        steps=27,
    )
)


no_symbol_bot_types = []

n = 0
while True:
    print("\n" * 3 * height)
    board = [[" "] * width for _ in range(height)]
    for b in current_bots:
        if b.position.x < 0 or b.position.x >= width:
            continue
        elif b.position.y < 0 or b.position.y >= height:
            continue
        if b.active:
            if hasattr(b, "symbol"):
                mark = b.symbol
            else:
                btype = b.__class__
                if btype not in no_symbol_bot_types:
                    no_symbol_bot_types.append(btype)
                mark = str(no_symbol_bot_types.index(btype) + 1)
            board[b.position.y][b.position.x] = mark
        else:
            board[b.position.y][b.position.x] = "\u2620"
    for row in board:
        print("".join(row))
    print("time={}".format(n))
    # input()       # uncomment this to pause for input after each frame
    time.sleep(0.2)

    for b in current_bots:
        b.update()
    n += 1
