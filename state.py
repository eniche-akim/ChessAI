#!/usr/bin/env python3
import numpy as np
import chess

class State:
    def __init__(self,board = None):
        if board is None: 
            self.board = chess.Board()
        else:
            self.board = board
    def serialize(self):
        assert self.board.is_valid()

        basic_state = np.zeros(64,np.uint8)

        for i in range(64):
            get_position = self.board.piece_at(i)
            #print(get_position)
            if get_position is not None:
                basic_state[i] = {"P":1, "N":2, "B":3, "R":4, "Q":5, "K":6, \
                               "p":9, "n":10, "b":11, "r":12, "q":13, "k":14} \
                        [get_position.symbol()]
                
            # print(basic_state)

        basic_state = basic_state.reshape(8,8)
        binary_state = np.zeros((5,8,8),np.uint8)
        # convert to binary representation
        binary_state[0] = (basic_state>>3)&1
        binary_state[1] = (basic_state>>2)&1
        binary_state[2] = (basic_state>>1)&1
        binary_state[3] = (basic_state>>0)&1
        
        binary_state[4] = int(self.board.turn)
        return binary_state

    def edges(self):
        return list(self.board.legal_moves)

    def values(self):
        return 1
    def key(self):
        return (self.board.board_fen(), self.board.turn, self.board.castling_rights, self.board.ep_square)



if __name__ == "__main__": 
    s = State()
    s.serialize()
