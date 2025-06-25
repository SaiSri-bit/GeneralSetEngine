import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from neural_network.layers.embedding import TokenEmbedding, PositionalEncoding
from neural_network.transformer import Transformer
from categories.matrix import Matrix, importMatrix
from constants import random


trainPath = "/Users/sri/Desktop/GeneralSetEngine/testing/time_series_data_test/train.csv"
trainMatrix = importMatrix(trainPath)
Columns = trainMatrix.X[0]
trainMatrix.deleteRow(0)
