from zipfile36 import ZipFile
import requests
from io import BytesIO
import pgn
import chess
import glob
import os

p_start = glob.glob("PGN\*")
for game in p_start:
   os.remove(game)
p_end = glob.glob("FEN\*")
for game in p_end:
   os.remove(game)

n = 1
count = 0
for i in range(n):
   pgn_id = 1437-i
   url = "http://theweekinchess.com/zips/twic%dg.zip"%pgn_id
   print(url)
   req = requests.get(url, headers={"User-Agent": "Microsoft Lumia 650"})
   zipfile = ZipFile(BytesIO(req.content))
   zipfile.extractall('PGN')
   f = open('./PGN/twic%d.pgn'%pgn_id)
   pgn_text = f.read()
   f.close()
   games = pgn.loads(pgn_text)
   for game in games:
      print(game.moves)
      board = chess.Board()
      ex = open("./FEN/Game%d.txt"%count,"w+")
      count = count + 1
      for move in game.moves[:-1]:
         board.push_san(move)
         fen = board.fen().split(" ", 1)[0]
         for r in range(8):
            fen = fen.replace("%d"%(r+1), "l"*(r+1))
         #fen = fen.split("/")
         ex.write(fen+"\n")
      ex.close()