# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:17:23 2023

@author: baudi
"""

while True:
    # p: your player number (0 to 1).
    p = input()
    xinit = [-1, -1]
    yinit = [-1, -1]
    xfina = [-1, -1]
    yfina = [-1, -1]
    for i in range(2):
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        xinit[i] = x0
        yinit[i] = y0
        xfina[i] = x1
        yfina[i] = y1
    # Décommenter cette ligne pour émuler un temps de réponse trop grand
    # time.sleep(20)
    if xinit[0] == 0:
        print("UP")
    else:
        print("DOWN")
