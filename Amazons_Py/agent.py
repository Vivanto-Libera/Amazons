import mcts
from Amazons import Board
import numpy as np

class Agent():

    def __init__(self, model):
        self.model = model

    def selectMove(self, board):
        rootEdge = mcts.Edge(None, None)
        rootEdge.N = 1
        rootNode = mcts.Node(board, rootEdge)
        mctsSearcher = mcts.MCTS(self.model, 50)
        moveProbs = mctsSearcher.search(rootNode)
        outputVec = {}
        for (move, prob) in moveProbs:
            outputVec[move[0]*10000+move[1]*100+move[2]] = prob
        vals = np.array(list(outputVec.values()))
        keys = np.array(list(outputVec.keys()))
        rand_idx = np.random.multinomial(1, vals)
        idx = np.where(rand_idx==1)[0][0]
        nextMove = keys[idx]
        return nextMove
