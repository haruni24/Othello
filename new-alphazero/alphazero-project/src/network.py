import torch
import torch.nn as nn
import torch.nn.functional as F

class PolicyValueNetwork(nn.Module):
    def __init__(self, board_size, num_channels):
        super(PolicyValueNetwork, self).__init__()
        self.conv1 = nn.Conv2d(1, num_channels, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(num_channels, num_channels, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(num_channels, num_channels, kernel_size=3, padding=1)
        self.policy_head = nn.Conv2d(num_channels, 2, kernel_size=1)  # 2 for the number of possible moves
        self.value_head = nn.Conv2d(num_channels, 1, kernel_size=1)

        self.fc_policy = nn.Linear(board_size * board_size * 2, 2)
        self.fc_value = nn.Linear(board_size * board_size, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        policy = self.policy_head(x)
        policy = policy.view(policy.size(0), -1)
        policy = F.softmax(self.fc_policy(policy), dim=1)

        value = self.value_head(x)
        value = value.view(value.size(0), -1)
        value = torch.tanh(self.fc_value(value))

        return policy, value

    def predict(self, board):
        board = torch.FloatTensor(board).unsqueeze(0).unsqueeze(0)  # Add batch and channel dimensions
        policy, value = self.forward(board)
        return policy.detach().numpy(), value.detach().numpy()