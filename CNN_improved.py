# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 20:44:53 2021

@author: Ali Masoumnia
"""

from torch import nn

class ConvNet(nn.Module):
    def __init__(self, vocab_length):
        super(ConvNet, self).__init__()
        
        classes = 2
        
        #convert document vector to 1000x1000
        self.length = nn.Linear(1, 100)
        self.width = nn.Linear(vocab_length, 100)

        self.block1 = nn.Sequential(
            #input size is (100, 100, 1)
            nn.Conv2d(in_channels=1, out_channels=5, kernel_size=26, stride=1, padding=0),
            #(75, 75, 5)
            nn.BatchNorm2d(num_features=5),
            nn.ReLU()
            )
        
        self.pool1 = nn.MaxPool2d(kernel_size=3)
            #(25, 25, 5)
        
        self.block2 = nn.Sequential(
            nn.Conv2d(in_channels=5, out_channels=10, kernel_size=6, stride=1, padding=0),
            #(20, 20, 5)
            nn.BatchNorm2d(num_features=10),
            nn.ReLU(),
            )
    
        self.pool2 = nn.MaxPool2d(kernel_size=5)
            #(4, 4, 10)
        
        self.fcblock = nn.Sequential(
            nn.Linear(in_features=4, out_features=1),
        )
        
        self.channelmap = nn.Linear(in_features=10, out_features=classes)
        self.prob = nn.Softmax(0)
    
    def forward(self, data):
        data = self.length(data.unsqueeze(1))
        data = self.width(data.T).unsqueeze(0).unsqueeze(1)
        
        out = self.block1(data)
        out = self.pool1(out)
        out = self.block2(out)
        out = self.pool2(out)
        print(out)
        print(out.shape)
        out = out.squeeze(0)
        out = self.fcblock(out).squeeze(2)
        out = out = self.fcblock(out)
        out = self.channelmap(out.T).squeeze()
        return self.prob(out)