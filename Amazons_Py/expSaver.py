import numpy as np
import os
import mcts
import torch
from Amazons import Board
from Amazons import State
from tqdm import tqdm
import numpy as np
from amazonsModel import AmazonsModel
import time
class ReinfLearn():

    def __init__(self, model):
        self.model = model

    def playGame(self):
        positionsData = []
        srcProbsData = []
        dstProbsData = []
        arrProbsData = []
        valuesData = []
        g = Board()
        while g.isTerminal() == State.EMPTY:
            positionsData.append(g.neuralworkInput())
            rootEdge = mcts.Edge(None, None)
            rootEdge.N = 1
            rootNode = mcts.Node(g, rootEdge)
            mctsSearcher = mcts.MCTS(self.model, 100)
            moveProbs = mctsSearcher.search(rootNode)
            outputVec = {}
            for (move, prob) in moveProbs:
                outputVec[move[0]*10000+move[1]*100+move[2]] = prob
            vals = np.array(list(outputVec.values()))
            keys = np.array(list(outputVec.keys()))
            rand_idx = np.random.multinomial(1, vals)
            idx = np.where(rand_idx==1)[0][0]
            nextMove = keys[idx]
            if(g.turn == State.WHITE):
                valuesData.append([1])
            else:
                valuesData.append([-1])
            src = np.zeros(100)
            dst = np.zeros(100)
            arr = np.zeros(100)
            for (m_tuple, prob) in moveProbs:
                src[m_tuple[0]] += prob
                dst[m_tuple[1]] += prob
                arr[m_tuple[2]] += prob
            src /= np.sum(src)
            srcProbsData.append(src)
            dst /= np.sum(dst)
            dstProbsData.append(dst)
            arr /= np.sum(arr)
            arrProbsData.append(arr)

            g.applyMove(nextMove)
        else:
            winner = g.isTerminal()
            for i in range(0, len(valuesData)):
                if(winner == State.BLACK):
                    valuesData[i][0] = valuesData[i][0] * -1.0
                else:
                    valuesData[i][0] = valuesData[i][0] * 1.0
        return (positionsData, srcProbsData, dstProbsData, arrProbsData, valuesData)
    
model = AmazonsModel()
thread = input("Which thread:")
i = 0
while True:
    if os.path.exists("model_exp"+str(i)+".pt"):
        model.load_state_dict(torch.load(f"model_exp{i}.pt"))
        learner = ReinfLearn(model)
        allPos = np.empty(0)
        allSrcProbs = np.empty(0)
        allDstProbs = np.empty(0)
        allArrProbs = np.empty(0)
        allValues = np.empty(0)
        for j in tqdm(range(0,10)):
            pos, srcProbs,dstProbs, arrProbs, values = learner.playGame()
            if allPos.size == 0:
                allPos = pos
                allSrcProbs = srcProbs
                allDstProbs = dstProbs
                allArrProbs = arrProbs
                allValues = values
            else:
                allPos = np.concatenate([pos, allPos], axis=0)
                allSrcProbs = np.concatenate([srcProbs, allSrcProbs], axis=0)
                allDstProbs = np.concatenate([dstProbs, allDstProbs], axis=0)
                allArrProbs = np.concatenate([arrProbs, allArrProbs], axis=0)
                allValues = np.concatenate([values, allValues], axis=0)
            allPos = np.concatenate([np.flip(pos, axis=-1), allPos], axis=0)
            allSrcProbs = np.concatenate([np.flip(srcProbs, axis=-1), allSrcProbs], axis=0)
            allDstProbs = np.concatenate([np.flip(dstProbs, axis=-1), allDstProbs], axis=0)
            allArrProbs = np.concatenate([np.flip(arrProbs, axis=-1), allArrProbs], axis=0)
            allValues = np.concatenate([values, allValues], axis=0)
        allPos = np.array(allPos)
        allSrcProbs = np.array(allSrcProbs)
        allDstProbs = np.array(allDstProbs)
        allArrProbs = np.array(allArrProbs)
        allValues = np.array(allValues)
        filePath = f'exp_tr{thread}_it{i}.npz'
        np.savez_compressed(
            filePath,
            pos=allPos,
            src=allSrcProbs,
            dst=allDstProbs,
            arr=allArrProbs,
            values=allValues
        )
        i += 1
    else:
        time.sleep(60)
    
