import torch
import numpy as np
from dataset import AmazonsDataset
from amazonsModel import AmazonsModel
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import os
import time

model = AmazonsModel()
model.load_state_dict(torch.load("model_exp0.pt"))
i = 0
policy_loss = nn.CrossEntropyLoss()
value_loss = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)
while True:

    if os.path.exists(f'exp_tr0_it{i}.npz') and os.path.exists(f'exp_tr1_it{i}.npz') and os.path.exists(f'exp_tr2_it{i}.npz') and os.path.exists(f'exp_tr3_it{i}.npz') and os.path.exists(f'exp_tr4_it{i}.npz'):
        allPos = np.empty(0)
        allSrcProbs = np.empty(0)
        allDstProbs = np.empty(0)
        allArrProbs = np.empty(0)
        allValues = np.empty(0)
        for j in range(0, 5):
            data = np.load(f'exp_tr{j}_it{i}.npz')
            if j == 0:
                allPos = data['pos']
                allSrcProbs = data['src']
                allDstProbs = data['dst']
                allArrProbs = data['arr']
                allValues = data['values']
            else:
                allPos = np.concatenate([data['pos'], allPos], axis=0)
                allSrcProbs = np.concatenate([data['src'], allSrcProbs], axis=0)
                allDstProbs = np.concatenate([data['dst'], allSrcProbs], axis=0)
                allArrProbs = np.concatenate([data['arr'], allArrProbs], axis=0)
                allValues = np.concatenate([data['values'], allValues], axis=0)
        train_dataset = AmazonsDataset(allPos, allSrcProbs, allDstProbs, allArrProbs, allValues)
        train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)
        device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        model.train()
        for epoch in range(0,10):
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
        i += 1
        torch.save(model.state_dict(), "model_exp"+str(i)+".pt")
        print("model saved")
    else:
        time.sleep(600)