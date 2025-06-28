import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from neural_network.layers.embedding import TokenEmbedding, PositionalEncoding
from neural_network.transformer import Transformer
from categories.matrix import Matrix, importMatrix
from constants import random


trainPath = "/Users/sri/Desktop/GeneralSetEngine/testing/time_series_data_test/train.csv"
trainMatrix = importMatrix(trainPath)
print(f'{trainMatrix.m} x {trainMatrix.n}')


trainMatrix.deleteColumn(0)
trainMatrix.deleteRow(0)

data = []
for rowM in trainMatrix.X:
    rowA = []
    for item in rowM:
        rowA.append(float(item))
    data.append(rowA)

src_list = data[:-1]
tgt_list = data[1:]

src = Matrix(matrix=src_list)
tgt = Matrix(matrix=tgt_list)

num_layers = 2
d_model = src.n
num_heads = 1
d_ff = d_model*2
transformer = Transformer(num_layers,d_model,num_heads,d_ff)

out = transformer.forward(src,tgt)

predicted_seq = out.X

for i, (actual_row, pred_row) in enumerate(zip(tgt_list, predicted_seq)):
        print(f"{i}\t{actual_row}\t{pred_row}")
