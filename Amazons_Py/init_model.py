import torch
import torch.nn as nn
from amazonsModel import AmazonsModel

model = AmazonsModel()
torch.save(model.state_dict(), 'init_model.pt')
