
from __future__ import print_function
import os
import chess
import time
import chess.svg
import traceback
import base64
from state import State
import torch
from train_model import ConvNetwork

class Valuator:
  def __init__(self, board = None):
    vals = torch.load("Data/value.pth", map_location=lambda storage, loc: storage)
    self.model = ConvNetwork() 
    self.model.load_state_dict(vals)

  def __call__(self, s):
    brd = s.serialize()
    brd = torch.tensor(brd)
    brd = brd.unsqueeze(0)
    output = self.model(brd.float())
    return float(output.data[0][0])

  def get_best_move(self, s, v):
    rated_moves = []
    for move in s.edges():
      s.board.push(move)
      value = v(s)
      rated_moves.append((value, move))
      s.board.pop()
    sorted_moves = sorted(rated_moves,reverse = s.board.turn)
    pourcentage = self.get_pourcentage(sorted_moves[0][0])
    return pourcentage ,sorted_moves[0][1]

  def get_pourcentage(self,valeur):
    	
    if valeur < 0:
  	  pourcentage = 50 + (-valeur*100 / 2)
    elif valeur > 0:
      pourcentage = (1 - valeur) * 100 / 2
    else:
  	  pourcentage = 50
    return pourcentage
	  	


