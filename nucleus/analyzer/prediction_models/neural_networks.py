import torch
import torch.nn as nn

class NeuralNetworks(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(13, 10)
        self.dropout1 = nn.Dropout(p=0.1)

        self.layer2 = nn.Linear(10, 5)
        self.dropout2 = nn.Dropout(p=0.1)

        self.layer3 = nn.Linear(5, 1)
            
        
        
    def forward(self, x):
        x = self.layer1(x)
        x = torch.relu(x)
        x = self.dropout1(x)

        x = self.layer2(x)
        x = torch.relu(x)
        x = self.dropout2(x)

        x = self.layer3(x)
        
        return x

model = NeuralNetworks()

x = torch.randn(1, 13)

criterion = nn.MSELoss()

target = torch.tensor([[0.60]])

