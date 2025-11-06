cimport cython
from libc.math cimport sqrt,pow
cimport numpy as np
import numpy as np
import math
from Amazons import Board
from Amazons import State
import random
import torch
from amazonsModel import AmazonsModel

ctypedef np.float32_t FLOAT32_t
ctypedef np.int32_t INT32_t

cdef class Edge():
    cdef:
        public Node parentNode
        public object move
        public int N
        public float W
        public float Q
        public float P
    def __init__(self, move, parentNode):
        self.parentNode = parentNode
        self.move = move
        self.N = 0 #visit counts
        self.W = 0.0 #sum of move values
        self.Q = 0.0 #move value
        self.P = 0.0 #prior probability

cdef class Node():
    cdef:
        public object board
        public Edge parentEdge
        public list childEdgeNode
    def __init__(self, board, parentEdge):
        self.board = board
        self.parentEdge = parentEdge
        self.childEdgeNode = []

    cpdef double expand(self, object network):
        cdef list moves = self.board.legalMoves()
        cdef int m
        cdef object child_board
        cdef Edge child_edge
        cdef Node childNode
        for m in moves:
            child_board = Board(self.board)
            child_board.applyMove(m)
            child_edge = Edge(m, self)
            childNode = Node(child_board, child_edge)
            self.childEdgeNode.append((child_edge,childNode))
        network.eval()
        cdef object device = torch.device("cpu")
        network = network.to(device)
        cdef object board_state = torch.FloatTensor(self.board.neuralworkInput()).unsqueeze(0)
        board_state = board_state.to(device)
        cdef:
            object q_src, q_arr,q_dst,q_vs
        with torch.no_grad():
            q_src,q_dst,q_arr,q_v = network(board_state)
        cdef float prob_sum = 0.0
        cdef Edge edge
        cdef Node _
        cdef int i
        cdef list m_idx
        for i in range(len(self.childEdgeNode)):
            edge, _ = self.childEdgeNode[i]
            m_idx = self.board.indexToMove(edge.move)
            edge.P = q_src[0, m_idx[0]*10+m_idx[1]] * q_dst[0, m_idx[2]*10+m_idx[3]] *q_arr[0, m_idx[4]*10+m_idx[5]]
            prob_sum += edge.P
        if prob_sum > 0:
            for i in range(len(self.childEdgeNode)):
                edge, _ = self.childEdgeNode[i]
                edge.P /= prob_sum
        cdef float v = q_v[0, 0]
        return v

    cpdef bint isLeaf(self):
        return self.childEdgeNode == []

cdef class MCTS():
    cdef:
        public object network
        public Node rootNode
        public double tau
        public double c_puct
        public int times
    def __init__(self, network, times):
        self.network = network
        self.rootNode = None
        self.tau = 1.0
        self.c_puct = 1.0 #some constant that adjust the impact of the overall bonus value u
        self.times = times

    @cython.cdivision(True)
    cpdef float uctValue(self, Edge edge, int parentN):
        return self.c_puct * edge.P * (sqrt(parentN) / (1+edge.N))

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef Node select(self, Node node):
        cdef:
            Node maxUctChild, child_node
            double maxUctValue, uctVal, uctValChild
            list allBestChilds
            int idx,i
            Edge edge
        if(node.isLeaf()):
            return node
        else:
            maxUctChild = None
            maxUctValue = -100000000.0
            for i in range(len(node.childEdgeNode)):
                edge, child_node = node.childEdgeNode[i]
                uctVal = self.uctValue(edge, edge.parentNode.parentEdge.N)
                val = edge.Q
                if(edge.parentNode.board.turn == State.BLACK):
                    val = -edge.Q
                uctValChild = val + uctVal
                if(uctValChild > maxUctValue):
                    maxUctChild = child_node
                    maxUctValue = uctValChild
            allBestChilds = []
            for i in range(len(node.childEdgeNode)):
                edge, child_node = node.childEdgeNode[i]
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

    cpdef void expandAndEvaluate(self, Node node):
        cdef:
            int winner
            double v
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

    cpdef void backup(self, float v, Edge edge):
        edge.N += 1
        edge.W = edge.W + v
        edge.Q = edge.W / edge.N
        if(edge.parentNode != None):
            if(edge.parentNode.parentEdge != None):
                self.backup(v, edge.parentNode.parentEdge)

    cpdef list search(self, Node rootNode):
        cdef:
            int i, N_sum, j
            double prob
            Edge edge
            Node node
            tuple m_tuple
            list m, moveProbs
        self.rootNode = rootNode
        self.rootNode.expand(self.network)
        for i in range(0, self.times):
            selected_node = self.select(rootNode)
            self.expandAndEvaluate(selected_node)
        N_sum = 0
        moveProbs = []
        for j in range(len(rootNode.childEdgeNode)):
            edge, _ = rootNode.childEdgeNode[j]
            N_sum += edge.N
        for j in range(len(rootNode.childEdgeNode)):
            edge, node = rootNode.childEdgeNode[j]
            prob = pow(edge.N, (1 / self.tau)) / pow(N_sum, (1/self.tau))
            m = Board.indexToMove(edge.move)
            m_tuple = (m[0]*10+m[1],m[2]*10+m[3],m[4]*10+m[5])
            moveProbs.append((m_tuple, prob))
        return moveProbs
