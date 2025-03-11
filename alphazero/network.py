import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class PVNet(nn.Module):
    def __init__(self):
        super(PVNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 128, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(128)
        self.bn2 = nn.BatchNorm2d(128)
        self.bn3 = nn.BatchNorm2d(128)
        self.bn4 = nn.BatchNorm2d(128)
        self.bn5 = nn.BatchNorm2d(128)
        self.fc1 = nn.Linear(128*8*8, 1024)
        self.policy_fc = nn.Linear(1024, 64)
        self.value_fc = nn.Linear(1024, 1)
        self.tanh = nn.Tanh()
        self.relu = nn.LeakyReLU(0.1)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        if x.dim()==3: x = x.unsqueeze(0)
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.relu(self.bn3(self.conv3(x)))
        x = self.relu(self.bn4(self.conv4(x)))
        x = self.relu(self.bn5(self.conv5(x)))
        x = x.view(-1, 128*8*8)
        x = self.relu(self.fc1(x))
        policy = self.softmax(self.policy_fc(x))
        value = self.tanh(self.value_fc(x))
        return policy, value
    
    def set_weights(self, weights):
        self.load_state_dict(weights)

    def get_weights(self):
        return self.state_dict()