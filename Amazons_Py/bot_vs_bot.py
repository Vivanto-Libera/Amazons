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
        board.applyMove(modelAgent.selectMove(board))
    winner = board.isTerminal()
    return winner


newWins = 0
oldWins = 0
model = AmazonsModel()
device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.load_state_dict(torch.load("new_model.pt",map_location=device))
model = model.to(device)

modelAgent = Agent(model)
g = Board()
print(bot_vs_bot(g))
