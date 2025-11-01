import torch
from torch.utils.data import Dataset
class AmazonsDataset(Dataset):
    def __init__(self, pos, y_src, y_dst,y_arr, y_value):
        self.pos = torch.tensor(pos, dtype=torch.float32)
        self.y_src = torch.tensor(y_src, dtype=torch.float32)
        self.y_dst = torch.tensor(y_dst, dtype=torch.float32)
        self.y_arr = torch.tensor(y_arr, dtype=torch.float32)
        self.y_value = torch.tensor(y_value, dtype=torch.float32)
    def __len__(self):
        return len(self.pos)
    def __getitem__(self, idx):
        return self.pos[idx], self.y_src[idx],self.y_sry_dstc[idx], self.y_arr[idx], self.y_value[idx]
