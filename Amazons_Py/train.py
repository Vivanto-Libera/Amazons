import mcts
import torch
from Amazons import Board
from Amazons import State
from tqdm import tqdm
import numpy as np
from dataset import AmazonsDataset
from amazonsModel import AmazonsModel
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn

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
                if(winner == Board.BLACK):
                    valuesData[i][0] = valuesData[i][0] * -1.0
                else:
                    valuesData[i][0] = valuesData[i][0] * 1.0
        return (positionsData, srcProbsData, dstProbsData, arrProbsData, valuesData)
    
model = AmazonsModel()
model.load_state_dict(torch.load("new_model.pt"))
policy_loss = nn.CrossEntropyLoss()
value_loss = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)
for i in range(0, 10000000):
    learner = ReinfLearn(model)
    allPos = []
    allSrcProbs = []
    allDstProbs = []
    allArrProbs = []
    allValues = []
    for j in tqdm(range(0,100)):
        pos, srcProbs,dstProbs, arrProbs, values = learner.playGame()
        allPos += pos
        allSrcProbs += srcProbs
        allDstProbs += dstProbs
        allArrProbs += arrProbs
        allValues += values
    allPos = np.array(allPos)
    allSrcProbs = np.array(allSrcProbs)
    allDstProbs = np.array(allDstProbs)
    allArrProbs = np.array(allArrProbs)
    allValues = np.array(allValues)
    train_dataset = AmazonsModel(allPos, allSrcProbs, allDstProbs, allArrProbs, allValues)
    train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)
    device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.train()
    for epoch in range(0,1):
        for batch_pos, batch_src,batch_dst,batch_arr,batch_val in train_loader:
            batch_pos = batch_pos.to(device)
            batch_src = batch_src.to(device)
            batch_dst = batch_dst.to(device)
            batch_arr = batch_arr.to(device)
            batch_val = batch_val.to(device)
            optimizer.zero_grad()
            pred_src, pred_dst, pred_arr, pred_value = model(batch_pos)
            loss_policy = policy_loss(pred_src, batch_src)
            loss_policy += policy_loss(pred_dst, batch_dst)
            loss_policy += policy_loss(pred_arr, batch_arr)
            loss_value = value_loss(pred_value, batch_val)
            loss = loss_policy + loss_value
            loss.backward()
            optimizer.step()
    torch.save(model.state_dict(), "model_it"+str(i)+".pt")
