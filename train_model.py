import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import h5py

class Dataset:
    def __init__(self, filename,length):
        self.x = None
        self.y = None
        self.len_dataset = length
        self.filename = filename
        self.load_model()

    def __getitem__(self, i):
        return (self.x[i], self.y[i])
    
    def __len__(self):
        return self.x.shape[0]
    
    def load_model(self):
        try:
            with h5py.File(self.filename,"r") as f:
                dataset_names = [n for n in f.keys()]
                self.x = f[dataset_names[0]][:self.len_dataset]
                self.y = f[dataset_names[1]][:self.len_dataset]
        except IOerror:
            print("error loading file")

class ConvNetwork(nn.Module):

    def __init__(self):
        super(ConvNetwork, self).__init__()
        self.a1 = nn.Conv2d(5,  64, kernel_size=2, padding=1)
        self.a2 = nn.Conv2d(64, 128, kernel_size=3, stride=2)

        self.b1 = nn.Conv2d(128, 192, kernel_size=3, padding=1)
        self.b2 = nn.Conv2d(192, 384, kernel_size=3, padding=1)
        self.b3 = nn.Conv2d(384, 384, kernel_size=3, stride=2)

        self.c1 = nn.Conv2d(384, 256, kernel_size=2, padding=1)
        self.c2 = nn.Conv2d(256, 256, kernel_size=2, stride=2)

        self.d2 = nn.Conv2d(256, 128, kernel_size=1)
        self.d3 = nn.Conv2d(128, 128, kernel_size=1)

        self.last = nn.Linear(128, 1)	

    def forward(self, x):
        x = F.relu(self.a1(x))
        x = F.relu(self.a2(x))

		# 4x4
        x = F.relu(self.b1(x))
        x = F.relu(self.b2(x))
        x = F.relu(self.b3(x))

        # 2x2
        x = F.relu(self.c1(x))
        x = F.relu(self.c2(x))

        # 1x128
        x = F.relu(self.d2(x))
        x = F.relu(self.d3(x))

        x = x.view(-1, 128)
        x = self.last(x)

        # value output
        return torch.tanh(x)

if __name__ == "__main__":
    device = "cpu"

    chess_dataset = Dataset("Data/Datasets.h5",5000000)
    train_loader = torch.utils.data.DataLoader(chess_dataset, batch_size= 256, shuffle=True)
    model = ConvNetwork()
    optimizer = optim.Adam(model.parameters())
    floss = nn.MSELoss()

    model.train()

    for epoch in range(100):
        all_loss = 0
        num_loss = 0
        for batch_idx, (data, target) in enumerate(train_loader):
            target = target.unsqueeze(-1)
            data, target = data.to(device), target.to(device)
            data = data.float()
            target = target.float()
            #print(target.size(), data.size())
            #print(data.shape, target.shape)
            optimizer.zero_grad()
            output = model(data)
            #print(output.shape)

            loss = floss(output, target)
            loss.backward()
            optimizer.step()

            all_loss += loss.item()
            num_loss += 1

        print("%3d: %f" % (epoch, all_loss/num_loss))
        torch.save(model.state_dict(), "Data/value2.pth")
