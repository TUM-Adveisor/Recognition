from zipfile36 import ZipFile
import requests
from io import BytesIO
import pgn
import chess
import glob
import numpy as np
import os

def translate(indices):
    move_games = []
    games = np.array(glob.glob("FEN\*"))[indices]
    for game in games:
        move_game = []
        with open(game, 'r') as f:
            og = 'rnbqkbnr/pppppppp/llllllll/llllllll/llllllll/llllllll/PPPPPPPP/RNBQKBNR'
            fen = f.readlines()
        fen.insert(0, og)
        for n in range(len(fen)-1):
            move_step = []
            diff = [i for i in range(len(fen[n])) if fen[n][i] != fen[n+1][i]]
            for pos in diff:
                if fen[n][pos]!="l":
                    for aim in diff:
                        if fen[n+1][aim]==fen[n][pos] and pos!=aim:
                            move_step.append([pos, aim])
                            if fen[n][aim]!="l":
                                move_step.append([aim, 100])
            if len(move_step)==0:
                for pos in diff:
                    if fen[n][pos]=="p" and fen[n][pos]=="P":
                        move_step.append([pos, 100])
                        move_step.append([100, pos+8])
            print(move_step)
            move_game.append(move_step)
        move_games.append(move_game)

translate([0])