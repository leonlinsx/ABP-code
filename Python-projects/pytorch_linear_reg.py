#!/usr/bin/env python
# coding: utf-8

# In[42]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# numpy generation of test and train sets

import numpy as np

# generate random x and y values
np.random.seed(42)
x = np.random.rand(100, 1)
y = 1 + 2 * x + 0.1 * np.random.randn(100, 1)

# shuffle a range of 1 - 100
idx = np.arange(100)
np.random.shuffle(idx)

# split to train and test sets for indices
train_idx = idx[:80]
val_idx = idx[80:]

# and use those shuffled indices to get train and test sets for x and y
x_train, y_train = x[train_idx], y[train_idx]
x_val, y_val = x[val_idx], y[val_idx]


# In[43]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# numpy implementation of linear reg

# initialise random params a and b
np.random.seed(42)
a = np.random.randn(1)
b = np.random.randn(1)

# sets learning rate
alpha = 0.1
# defines number of epochs
n_epochs = 1000

for epoch in range(n_epochs):
    # compute model predicted output
    yhat = a + b * x_train
    
    # calc error from actual minus predicted
    error = y_train - yhat
    # calc mean squared error
    loss = (error ** 2).mean()
    
    # calc gradient for a and b (-2 divided by N * summation to N of y - y hat, or x * (y - y hat))
    a_grad = -2 * error.mean()
    b_grad = -2 * (x_train * error).mean()
    
    # update a and b
    a = a - alpha * a_grad
    b = b - alpha * b_grad
    
# print(a, b)

# Sanity check with sklearn   
# from sklearn.linear_model import LinearRegression
# regressor = LinearRegression()
# regressor.fit(x_train, y_train)
# print(regressor.intercept_, regressor.coef_[0])


# In[44]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# pytorch implementation of linear reg v1, just using loss

import gpytorch  # Uber data session required
import torch
import torch.optim as optim
import torch.nn as nn
from torchviz import make_dot

# set to correct device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# data was in numpy arrays, need to transform to pytorch tensor, and send to device
x_train_tensor = torch.from_numpy(x_train).float().to(device)
y_train_tensor = torch.from_numpy(y_train).float().to(device)

# sets learning rate
alpha = 0.1
# defines number of epochs
n_epochs = 1000

# better to specify device at moment of creation (more applicable w/ gpu)
torch.manual_seed(42)
a = torch.randn(1, requires_grad=True, dtype=torch.float, device=device)
b = torch.randn(1, requires_grad=True, dtype=torch.float, device=device)
# print(a, b)

for epoch in range(n_epochs):
    yhat = a + b * x_train_tensor
    error = y_train_tensor - yhat
    #  calc error and mean sq error from tensors
    loss = (error ** 2).mean()
    
    # work backwards from specified loss to calc gradient for all
    loss.backward()
    
    # update a and b 
    # need to use no_grad to keep update out of gradient computatoiin
    # due to dynamic graph pytorch uses
    with torch.no_grad():
        a -= alpha * a.grad
        b -= alpha * b.grad
    
    # pytorch is clingy to computed gradients, need to let them go
    a.grad.zero_()
    b.grad.zero_()

# print(a, b)


# In[45]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# pytorch implementation of linear reg v2, usinig loss and optimizer

# sets learning rate
alpha = 0.1
# defines number of epochs
n_epochs = 1000

# better to specify device at moment of creation (more applicable w/ gpu)
torch.manual_seed(42)
a = torch.randn(1, requires_grad=True, dtype=torch.float, device=device)
b = torch.randn(1, requires_grad=True, dtype=torch.float, device=device)
# print(a, b)

# define a SGD optimizer
# says stochastic grad descent, but if you run on all batch it'll be a batch
optimizer = optim.SGD([a, b], lr=alpha)

for epoch in range(n_epochs):
    yhat = a + b * x_train_tensor
    error = y_train_tensor - yhat
    #  calc error and mean sq error from tensors
    loss = (error ** 2).mean()
    
    # work backwards from specified loss to calc gradient for all
    loss.backward()
    
    # update a and b, no need to update manually 
    optimizer.step()
    
    # no need to set individually
    optimizer.zero_grad()

# print(a, b)


# In[46]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# pytorch implementation of linear reg v3, using loss, loss function, and optimizer

# sets learning rate
alpha = 0.1
# defines number of epochs
n_epochs = 1000

# better to specify device at moment of creation (more applicable w/ gpu)
torch.manual_seed(42)
a = torch.randn(1, requires_grad=True, dtype=torch.float, device=device)
b = torch.randn(1, requires_grad=True, dtype=torch.float, device=device)
print(a, b)

# define a mean sq err loss functioni
loss_fn = nn.MSELoss(reduction='mean')

# define a SGD optimizer
# says stochastic grad descent, but if you run on all batch it'll be a batch
optimizer = optim.SGD([a, b], lr=alpha)

for epoch in range(n_epochs):
    yhat = a + b * x_train_tensor

    # no need to manually update
    loss = loss_fn(y_train_tensor, yhat)
    
    # work backwards from specified loss to calc gradient for all
    loss.backward()
    
    # update a and b, no need to update manually 
    optimizer.step()
    
    # no need to set individually
    optimizer.zero_grad()

print(a, b)


# In[47]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# pytorch implementation of linear reg v4, defining model beforehand

class ManualLinearRegression(nn.Module):
    # def parts that make up model
    def __init__(self):
        super().__init__()
        # need to wrap a and b params with nn.Parameter
        self.a = nn.Parameter(torch.randn(1, requires_grad=True, dtype=torch.float, device=device))
        self.b = nn.Parameter(torch.randn(1, requires_grad=True, dtype=torch.float, device=device))
        
    # performs computation and returns prediction    
    def forward(self, x):
        return self.a + self.b * x
    
torch.manual_seed(42)

# now we can create model and sendd to device 
model = ManualLinearRegression().to(device)
# can inspect params with state_dict
print(model.state_dict())

# sets learning rate
alpha = 0.1
# defines number of epochs
n_epochs = 1000

# define a mean sq err loss function
loss_fn = nn.MSELoss(reduction='mean')

# define a SGD optimizer
# says stochastic grad descent, but if you run on all batch it'll be a batch
optimizer = optim.SGD(model.parameters(), lr=alpha)

for epoch in range(n_epochs):
    # does not perform training; just sets model to training mode
    model.train()
    
    # no more manual prediction
    yhat = model(x_train_tensor)
    
    # no need to manually update
    loss = loss_fn(y_train_tensor, yhat)
    
    # work backwards from specified loss to calc gradient for all
    loss.backward()
    
    # update a and b, no need to update manually 
    optimizer.step()
    
    # no need to set individually
    optimizer.zero_grad()
    
print(model.state_dict())


# In[48]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# pytorch implementation of linear reg v5, with function that takes optimizer, loss, and model

class ManualLinearRegression(nn.Module):
    # def parts that make up model
    def __init__(self):
        super().__init__()
        # need to wrap a and b params with nn.Parameter
        self.a = nn.Parameter(torch.randn(1, requires_grad=True, dtype=torch.float, device=device))
        self.b = nn.Parameter(torch.randn(1, requires_grad=True, dtype=torch.float, device=device))
        
    # performs computation and returns prediction    
    def forward(self, x):
        return self.a + self.b * x

def make_train_step(model, loss_fn, optimizer):
    # build function to perform step in train loop
    def train_step(x, y):
        # set model to train
        model.train()
        # make prediction
        yhat = model(x)
        # compute loss
        loss = loss_fn(y, yhat)
        # compute gradient
        loss.backward()
        # update params, zeros gradients
        optimizer.step()
        optimizer.zero_grad()
        # return loss
        return loss.item()
    
    # return function called inside the train loop
    return train_step

torch.manual_seed(42)

# now we can create model and sendd to device 
model = ManualLinearRegression().to(device)

# sets learning rate
alpha = 0.1
# defines number of epochs
n_epochs = 1000

# define a mean sq err loss function
loss_fn = nn.MSELoss(reduction='mean')

# define a SGD optimizer
# says stochastic grad descent, but if you run on all batch it'll be a batch
optimizer = optim.SGD(model.parameters(), lr=alpha)

# create train_step function for model, loss_fn, optimizer
train_step = make_train_step(model, loss_fn, optimizer)
losses = []

# run through all epochs
for epoch in range(n_epochs):
    # perform one train step and return loss
    loss = train_step(x_train_tensor, y_train_tensor)
    losses.append(loss)
    
print(model.state_dict())


# In[49]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# pytorch implementation of linear reg v6, building dataset

from torch.utils.data import Dataset, TensorDataset

class CustomDataset(Dataset):
    def __init__(self, x_tensor, y_tensor):
        self.x = x_tensor
        self.y = y_tensor
    
    def __getitem__(self, index):
        return (self.x[index], self.y[index])
    
    def __len__(self):
        return len(self.x)    
    
# built training tensors out of numpy arrays, but didn't send to device
# dont want to load whole training data in GPU as takes up RAM
x_train_tensor = torch.from_numpy(x_train).float()
y_train_tensor = torch.from_numpy(y_train).float()

train_data = CustomDataset(x_train_tensor, y_train_tensor)
print(train_data[0])

# if dataset is only a few tensors, can use pytorch tensordataset
# train_data = TensorDataset(x_train_tensor, y_train_tensor)
# print(train_data[0])

from torch.utils.data import DataLoader

# tell the loader what dataset, batch size, and to shuffle
# can loop over this to get different batch each time for mini-batch grad descent
train_loader = DataLoader(dataset=train_data, batch_size=16, shuffle=True)

# create train_step function for model, loss_fn, optimizer
train_step = make_train_step(model, loss_fn, optimizer)
losses = []

for epoch in range(n_epochs):
    for x_batch, y_batch in train_loader:
        # dataset lives in CPU, so do mini batches
        # need to send mini batches to device where model lives
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        
        loss = train_step(x_batch, y_batch)
        losses.append(loss)

print(model.state_dict())


# In[50]:


# lesson from https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e
# pytorch implementation of linear reg v7 alternative way of doing training val split

from torch.utils.data.dataset import random_split

x_tensor = torch.from_numpy(x).float()
y_tensor = torch.from_numpy(y).float()

dataset = TensorDataset(x_tensor, y_tensor)

# train test split
train_dataset, val_dataset = random_split(dataset, [80, 20])

train_loader = DataLoader(dataset=train_dataset, batch_size=16)
val_loader = DataLoader(dataset=val_dataset, batch_size=20)

losses = []
val_losses = []
train_step = make_train_step(model, loss_fn, optimizer)

for epoch in range(n_epochs):
    for x_batch, y_batch in train_loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        
        loss = train_step(x_batch, y_batch)
        losses.append(loss)

    with torch.no_grad():
        for x_val, y_val in val_loader:
            x_val = x_val.to(device)
            y_val - y_val.to(device)
            
            model.eval()
            
            yhat = model(x_val)
            val_loss = loss_fn(y_val, yhat)
            val_losses.append(val_loss.item())

print(model.state_dict())


# In[51]:


# full pytorch implementation with train val split, custom dataset, train step
# https://gist.github.com/dvgodoy/1d818d86a6a0dc6e7c07610835b46fe4#gistcomment-2998244

import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn
from torchviz import make_dot
from torch.utils.data import Dataset, TensorDataset, DataLoader
from torch.utils.data.dataset import random_split

device = 'cuda' if torch.cuda.is_available() else 'cpu'

np.random.seed(42)
x = np.random.rand(100, 1)
true_a, true_b = 1, 2
y = true_a + true_b*x + 0.1*np.random.randn(100, 1)

x_tensor = torch.from_numpy(x).float()
y_tensor = torch.from_numpy(y).float()

class CustomDataset(Dataset):
    def __init__(self, x_tensor, y_tensor):
        self.x = x_tensor
        self.y = y_tensor

    def __getitem__(self, index):
        return (self.x[index], self.y[index])

    def __len__(self):
        return len(self.x)

dataset = TensorDataset(x_tensor, y_tensor) # dataset = CustomDataset(x_tensor, y_tensor)

train_dataset, val_dataset = random_split(dataset, [80, 20])

train_loader = DataLoader(dataset=train_dataset, batch_size=16)
val_loader = DataLoader(dataset=val_dataset, batch_size=20)

class ManualLinearRegression(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

def make_train_step(model, loss_fn, optimizer):
    def train_step(x, y):
        model.train()
        yhat = model(x)
        loss = loss_fn(y, yhat)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        return loss.item()
    return train_step

# Estimate a and b
torch.manual_seed(42)

model = ManualLinearRegression().to(device) # model = nn.Sequential(nn.Linear(1, 1)).to(device)
loss_fn = nn.MSELoss(reduction='mean')
optimizer = optim.SGD(model.parameters(), lr=1e-1)
train_step = make_train_step(model, loss_fn, optimizer)

n_epochs = 100
training_losses = []
validation_losses = []
print(model.state_dict())

for epoch in range(n_epochs):
    batch_losses = []
    for x_batch, y_batch in train_loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        loss = train_step(x_batch, y_batch)
        batch_losses.append(loss)
    training_loss = np.mean(batch_losses)
    training_losses.append(training_loss)

    with torch.no_grad():
        val_losses = []
        for x_val, y_val in val_loader:
            x_val = x_val.to(device)
            y_val = y_val.to(device)
            model.eval()
            yhat = model(x_val)
            val_loss = loss_fn(y_val, yhat).item()
            val_losses.append(val_loss)
        validation_loss = np.mean(val_losses)
        validation_losses.append(validation_loss)

#     print(f"[{epoch+1}] Training loss: {training_loss:.3f}\t Validation loss: {validation_loss:.3f}")

print(model.state_dict())

