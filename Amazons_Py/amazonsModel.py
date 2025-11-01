import torch
import torch.nn as nn
import torch.nn.functional as F

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.feature = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
        )
    def forward(self, x):
        r = self.feature(x)
        return F.relu(x + r)



class AmazonsModel(nn.Module):
    def __init__(self):
        super(AmazonsModel, self).__init__()
        self.stem = nn.Sequential(
            nn.Conv2d(4, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            )
        self.resblocks = nn.Sequential(
            *[ResidualBlock(128) for _ in range(0, 4)]
        )
        self.src_head = nn.Sequential(
            nn.Conv2d(128, 32, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 1, 1),
        )
        self.dst_head = nn.Sequential(
            nn.Conv2d(256, 32, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32,1,1)
        )
        self.arr_head = nn.Sequential(
            nn.Conv2d(384, 32,3,padding=1),
            nn.ReLU(),
            nn.Conv2d(32,1,1)
        )
        self.value_head = nn.Sequential(
            nn.Conv2d(128, 128,1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256,1),
            nn.Tanh()
            )
    def forward(self, x):
        B, C, H, W = x.shape
        x =  self.stem(x)
        x = self.resblocks(x)
        v = self.value_head(x)
        src_logits = self.src_head(x).flatten(1)
        src_prob = F.softmax(src_logits, dim=1).view(B,1,H,W)
        src_context = torch.sum(src_prob * x, dim=(2,3), keepdim=True)
        dst_in = torch.cat([x, src_context.expand(-1,-1,H,W)], dim=1)
        dst_logits = self.dst_head(dst_in).flatten(1)
        dst_prob = F.softmax(dst_logits, dim=1).view(B,1,H,W)
        dst_context = torch.sum(dst_prob * x, dim=(2,3), keepdim=True)
        arr_in = torch.cat([x, dst_context.expand(-1,-1,H,W)], dim=1)
        arr_logits = self.dst_head(arr_in).flatten(1)
        return F.softmax(src_logits, dim=1), F.softmax(dst_logits, dim=1), F.softmax(arr_logits, dim=1), v
        
