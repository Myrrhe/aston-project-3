import sys
import math


# game looppp test2
while True:
    # p: your player number (0 to 1).
    p = int(input())
    for i in range(2):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1 = [int(j) for j in input().split()]

    # A single line with UP, DOWN, LEFT or RIGHT
    print("LEFT")