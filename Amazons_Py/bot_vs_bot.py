import torch
from Amazons import Board
from Amazons import State
from agent import Agent
from tqdm import tqdm
from amazonsModel import AmazonsModel
from print_board import print_board

def bot_vs_bot(board):
    while(board.isTerminal() == State.EMPTY):
        print_board(board)
        if(board.turn == State.WHITE):
            board.applyMove(modelAgent.selectMove(board))
            continue
        else:
            board.applyMove(modelAgent.selectMove(board))
            continue
    terminal, winner = board.isTerminal()
    return winner


newWins = 0
oldWins = 0
model = AmazonsModel()
device= torch.device("cpu")
model.load_state_dict(torch.load("new_model.pt",map_location=device))
model = model.to(device)

modelAgent = Agent(model)
g = Board()
bot_vs_bot(g)
