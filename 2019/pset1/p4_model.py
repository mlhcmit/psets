# Based heavily on https://github.com/bentrevett/pytorch-sentiment-analysis/blob/master/4%20-%20Convolutional%20Sentiment%20Analysis.ipynb

import torch
from torchtext import data
from torchtext import datasets
import random
import spacy
import time


SEED = 1234

torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True


start = time.time()

TEXT = data.Field(tokenize='spacy', sequential=True)
LABEL = data.LabelField(dtype=torch.float)

import sys
import csv

csv.field_size_limit(sys.maxsize)


train_data, valid_data, test_data = data.TabularDataset.splits(
        path='./', train='train.csv', validation='valid.csv', test='test.csv', 
        skip_header=True, format='csv',
        fields=[('id', None), ('text', TEXT), ('label', LABEL)])

ckpt1 = time.time()
print 'checkpoint 1: %d' % (ckpt1 - start)

# train_data, test_data = datasets.IMDB.splits(TEXT, LABEL)

# train_data, valid_data = train_data.split(random_state=random.seed(SEED))

# print 'data prepared'

TEXT.build_vocab(train_data, max_size=5000, vectors="glove.6B.100d")
LABEL.build_vocab(train_data)

ckpt2 = time.time()
print 'checkpoint 2: %d' % (ckpt2 - start)


BATCH_SIZE = 64

device = torch.device('cpu')

# # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

train_iterator, valid_iterator, test_iterator = data.BucketIterator.splits(
    (train_data, valid_data, test_data), 
    batch_size=BATCH_SIZE, 
    device=device)

import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, n_filters, filter_sizes, output_dim, dropout):
        super(CNN, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.convs = nn.ModuleList([nn.Conv2d(in_channels=1, out_channels=n_filters, kernel_size=(fs,embedding_dim)) for fs in filter_sizes])
        self.fc = nn.Linear(len(filter_sizes)*n_filters, output_dim)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        x = x.permute(1, 0)
        embedded = self.embedding(x)
        embedded = embedded.unsqueeze(1)
        conved = [F.relu(conv(embedded)).squeeze(3) for conv in self.convs]
        pooled = [F.max_pool1d(conv, conv.shape[2]).squeeze(2) for conv in conved]
        cat = self.dropout(torch.cat(pooled, dim=1))
    
        return self.fc(cat)

INPUT_DIM = len(TEXT.vocab)
EMBEDDING_DIM = 100
N_FILTERS = 100
FILTER_SIZES = [3,4,5]
OUTPUT_DIM = 1
DROPOUT = 0.5

model = CNN(INPUT_DIM, EMBEDDING_DIM, N_FILTERS, FILTER_SIZES, OUTPUT_DIM, DROPOUT)

pretrained_embeddings = TEXT.vocab.vectors

model.embedding.weight.data.copy_(pretrained_embeddings)

print 'train model'

import torch.optim as optim

optimizer = optim.Adam(model.parameters())

criterion = nn.BCEWithLogitsLoss()

model = model.to(device)
criterion = criterion.to(device)

ckpt3 = time.time()
print 'checkpoint 3: %d' % (ckpt3 - start)


def binary_accuracy(preds, y):
    """
    Returns accuracy per batch, i.e. if you get 8/10 right, this returns 0.8, NOT 8
    """

    #round predictions to the closest integer
    rounded_preds = torch.round(torch.sigmoid(preds))
    correct = (rounded_preds == y).float() #convert into float for division 
    acc = correct.sum()/len(correct)
    return acc

def train(model, iterator, optimizer, criterion):
    
    epoch_loss = 0
    epoch_acc = 0
    
    model.train()
    
    for batch in iterator:
        
        optimizer.zero_grad()
        
        predictions = model(batch.text).squeeze(1)
        
        loss = criterion(predictions, batch.label)
        
        acc = binary_accuracy(predictions, batch.label)
        
        loss.backward()
        
        optimizer.step()
        
        epoch_loss += loss.item()
        epoch_acc += acc.item()
        
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

def evaluate(model, iterator, criterion):
    
    epoch_loss = 0
    epoch_acc = 0
    
    model.eval()
    
    with torch.no_grad():
    
        for batch in iterator:

            predictions = model(batch.text).squeeze(1)
            
            loss = criterion(predictions, batch.label)
            
            acc = binary_accuracy(predictions, batch.label)

            epoch_loss += loss.item()
            epoch_acc += acc.item()
        
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

N_EPOCHS = 5

for epoch in range(N_EPOCHS):
    train_loss, train_acc = train(model, train_iterator, optimizer, criterion)
    valid_loss, valid_acc = evaluate(model, valid_iterator, criterion)
    
    print '| Epoch: %d | Train Loss: %.3f | Train Acc: %.2f | Val. Loss: %.3f | Val. Acc: %.2f |' % (epoch, train_loss, train_acc * 100, valid_loss, valid_acc * 100)
    
ckpt4 = time.time()
print 'checkpoint 4: %d' % (ckpt4 - start)

test_loss, test_acc = evaluate(model, test_iterator, criterion)
print '| Test Loss: %.3f | Test Acc: %.2f |' % (test_loss, test_acc * 100)

finish = time.time()
print 'finish: %d' % (finish - start)

torch.save(model.state_dict(), 'pretrained_model.pt')
# import pdb; pdb.set_trace()
