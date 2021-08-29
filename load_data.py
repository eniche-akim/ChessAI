import chess.pgn
import os
from state import State
import numpy as np
import h5py as h5

def load_and_serialize_data(folder_name):


    f = h5.File(os.path.join(folder_name, 'Datasets.h5'),'w')
    all_files = [os.path.join(folder_name,file_name) \
                 for file_name in os.listdir(folder_name) \
                 if os.path.isfile(os.path.join(folder_name,file_name ))]

    i=0
    for file_name in all_files:
        pgn_file = open(file_name)
        while True:
            try:
                game = chess.pgn.read_game(pgn_file)
                Data, Labels = [], []
            except Exception:
                break
        
            value = {'1/2-1/2': 0, '1-0': 1, '0-1':-1}[game.headers["Result"]] 
            board = game.board()
        
            for move in game.mainline_moves():
                board.push(move)
                ser = State(board).serialize()
                Data.append(ser)
                Labels.append(value)
            Data = np.array(Data)
            Labels = np.array(Labels)
            if Data.size != 0:
                #print(Data, Labels)
                print("number of games %d, examples %d"% (i,len(Labels)))
                if i == 0:
                    f.create_dataset('data', data = Data, compression = "gzip",chunks = True, maxshape = (None, 5, 8, 8))
                    f.create_dataset('labels', data = Labels, compression = "gzip",chunks = True,maxshape = (None,))
                else:
                    f['data'].resize((f['data'].shape[0] + Data.shape[0]), axis=0)
                    f['data'][-Data.shape[0]:] = Data

                    f['labels'].resize((f['labels'].shape[0] + Labels.shape[0]), axis=0)
                    f['labels'][-Labels.shape[0]:] = Labels
                i = i + 1
    
    f.close() 


if __name__ == "__main__":

   load_and_serialize_data("Data")
