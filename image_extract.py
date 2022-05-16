import cv2
import numpy as np
import matplotlib.pyplot as plt
from chessboard import find_intersection
import glob
import os

pieces = glob.glob("dataset\*")
for P in pieces:
    piece = glob.glob(P+"\*")
    for p in piece:
        os.remove(p)

intersection, height = find_intersection()
images = glob.glob("raw_data\*")
count = 0
for i in images:
    image = cv2.imread(i)
    piece_dict = {
        "r": "br",
        "n": "bn",
        "b": "bb",
        "k": "bk",
        "q": "bq",
        "p": "bp",
        "l": "l",
        "P": "wp",
        "R": "wr",
        "N": "wn",
        "B": "wb",
        "Q": "wq",
        "K": "wk"
    }
    position = ["rnbkqbnr", "pppppppp", "llllllll", "llllllll", "llllllll", "llllllll", "PPPPPPPP", "RNBQKBNR"]
    for i in range(len(intersection)-1):
        for j in range(len(intersection[i])-1):
            w_s = int(intersection[i][j+1][0])
            w_e = int(intersection[i+1][j][0])
            h_e = int(intersection[i][j][1])
            h_s = h_e-int(height[i][j])
            crop = image[h_s:h_e, w_s:w_e]
            cv2.imwrite("dataset/"+piece_dict[position[j][i]]+"/%d%d%d.jpg"%(count,i,j), crop)
    count = count+1