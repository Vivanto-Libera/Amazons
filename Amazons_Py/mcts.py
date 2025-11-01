import copy
import numpy as np
import math
from Amazons import Board
from Amazons import State
import random
import torch
from amazonsModel import AmazonsModel

class Edge():
    def __init__(self, move, parentNode):
        self.parentNode = parentNode
        self.move = move
        self.N = 0 #visit counts
        self.W = 0 #sum of move values
        self.Q = 0 #move value
        self.P = 0 #prior probability

class Node():
    def __init__(self, board, parentEdge):
        self.board = board
        self.parentEdge = parentEdge
        self.childEdgeNode = []

    def expand(self, network):
        moves = self.board.legalMoves()
        for m in moves:
            child_board = Board(self.board)
            child_board.applyMove(m)
            child_edge = Edge(m, self)
            childNode = Node(child_board, child_edge)
            self.childEdgeNode.append((child_edge,childNode))
        network.eval()
        device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
        network = network.to(device)
        board_state = torch.FloatTensor(self.board.neuralworkInput()).unsqueeze(0)
        board_state = board_state.to(device)
        with torch.no_grad():
            q_src,q_dst,q_arr,q_v = network(board_state)
        prob_sum = 0.
        for (edge,_) in self.childEdgeNode:
            m_idx = self.board.indexToMove(edge.move)
            edge.P = q_src[0, m_idx[0]*10+m_idx[1]] * q_dst[0, m_idx[2]*10+m_idx[3]] *q_arr[0, m_idx[4]*10+m_idx[5]]
            prob_sum += edge.P
        for edge,_ in self.childEdgeNode:
            edge.P /= prob_sum
        v = q_v[0, 0]
        return v

    def isLeaf(self):
        return self.childEdgeNode == []
    
class MCTS():

    def __init__(self, network, times):
        self.network = network
        self.rootNode = None
        self.tau = 1.0
        self.c_puct = 1.0 #some constant that adjust the impact of the overall bonus value u
        self.times = times

    def uctValue(self, edge, parentN):
        return self.c_puct * edge.P * (math.sqrt(parentN) / (1+edge.N))

    def select(self, node):
        if(node.isLeaf()):
            return node
        else:
            maxUctChild = None
            maxUctValue = -100000000.
            for edge, child_node in node.childEdgeNode:
                uctVal = self.uctValue(edge, edge.parentNode.parentEdge.N)
                val = edge.Q
                if(edge.parentNode.board.turn == State.BLACK):
                    val = -edge.Q
                uctValChild = val + uctVal
                if(uctValChild > maxUctValue):
                    maxUctChild = child_node
                    maxUctValue = uctValChild
            allBestChilds = []
            for edge, child_node in node.childEdgeNode:
                uctVal = self.uctValue(edge, edge.parentNode.parentEdge.N)
                val = edge.Q
                if(edge.parentNode.board.turn == State.BLACK):
                    val = -edge.Q
                uctValChild = val + uctVal
                if(uctValChild == maxUctValue):
                    allBestChilds.append(child_node)
            if(maxUctChild == None):
                raise ValueError("could not identify child with best uct value")
            else:
                if(len(allBestChilds) > 1):
                    idx = random.randint(0, len(allBestChilds)-1)
                    return self.select(allBestChilds[idx])
                else:
                    return self.select(maxUctChild)
                
    def expandAndEvaluate(self, node):
        winner = node.board.isTerminal()
        if(winner != State.EMPTY):
            v = 0.0
            if(winner == State.WHITE):
                v = 1.0
            if(winner == State.BLACK):
                v = -1.0
            self.backup(v, node.parentEdge)
            return
        v = node.expand(self.network)
        self.backup(v, node.parentEdge)

    def backup(self, v, edge):
        edge.N += 1
        edge.W = edge.W + v
        edge.Q = edge.W / edge.N
        if(edge.parentNode != None):
            if(edge.parentNode.parentEdge != None):
                self.backup(v, edge.parentNode.parentEdge)

    def search(self, rootNode):
        self.rootNode = rootNode
        self.rootNode.expand(self.network)
        for i in range(0, self.times):
            selected_node = self.select(rootNode)
            self.expandAndEvaluate(selected_node)
        N_sum = 0
        moveProbs = []
        for edge, _ in rootNode.childEdgeNode:
            N_sum += edge.N
        for (edge, node) in rootNode.childEdgeNode:
            prob = (edge.N ** (1 / self.tau)) / ((N_sum) ** (1/self.tau))
            m = Board.indexToMove(edge.move)
            m_tuple = (m[0]*10+m[1],m[2]*10+m[3],m[4]*10+m[5])
            moveProbs.append((m_tuple, prob))
        return moveProbs
