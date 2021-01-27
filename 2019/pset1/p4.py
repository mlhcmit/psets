"""
Part 4 of MLHC 2019 Pset 1

This file shows you how to build the vocab and model and then load
the pretrained weights.

Note that this script takes ~20 minutes on a laptop since building
the vocabulary is non-trivial. 
"""
import torch

from torchtext import data

from models import CNN

import time
import sys
import csv
import math
import numpy as np
import pandas as pd

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
 

start = time.time()

TEXT = data.Field(tokenize='spacy', sequential=True)
LABEL = data.LabelField(dtype=torch.float)
ID = data.Field(sequential=False, use_vocab=False,is_target=False)

csv.field_size_limit(sys.maxsize)


train_data, valid_data, test_data = data.TabularDataset.splits(
        path='./', train='train.csv', validation='valid.csv', test='test.csv', 
        skip_header=True, format='csv',
        fields=[('id', ID), ('text', TEXT) , ('label', LABEL)])
#     fields=[('text', TEXT) , ('label', LABEL)])

TEXT.build_vocab(train_data, max_size=5000, vectors="glove.6B.100d")
LABEL.build_vocab(train_data)

BATCH_SIZE = 64
device = torch.device('cpu')

train_iterator, valid_iterator, test_iterator = data.BucketIterator.splits(
    (train_data, valid_data, test_data), 
    batch_size=BATCH_SIZE, 
    device=device)


INPUT_DIM = len(TEXT.vocab)
# INPUT_DIM = 5002
EMBEDDING_DIM = 100
N_FILTERS = 100
FILTER_SIZES = [3,4,5]
OUTPUT_DIM = 1
DROPOUT = 0.5

model = CNN(INPUT_DIM, EMBEDDING_DIM, N_FILTERS, FILTER_SIZES, OUTPUT_DIM, DROPOUT)

# def get_preds(model, iterator):    
    
#                 yield pred

ck1 = time.time()
print '1: %.3f' % (ck1-start)

model.load_state_dict(torch.load('pretrained_model.pt'))

import pdb; pdb.set_trace()

model.eval()
all_preds = np.zeros(len(test_data))
all_ids = np.zeros(len(test_data))
all_labels = np.zeros(len(test_data))

with torch.no_grad():
    i = 0
    for batch in test_iterator:
        predictions = model(batch.text).squeeze(1)
        
        for j,pred in enumerate(predictions):
            all_preds[i] = sigmoid(pred.numpy())
            all_labels[i] = batch.label[j].numpy()
            all_ids[i] = batch.id[j].numpy()
            i += 1
            
ck2 = time.time()
print 'ck2: %.3f' % (ck2-start)


df = pd.DataFrame({
    'label': all_labels, 'preds': all_preds,
    'id': all_ids
})

df.to_csv('cnn_preds.csv', index=False)
