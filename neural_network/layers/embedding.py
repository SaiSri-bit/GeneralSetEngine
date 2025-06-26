import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from categories.Category import Object
from categories.matrix import Matrix
from constants import sin,cos


class TokenEmbedding(Object):
    def __init__(self, vocab_size: int, d_model: int):
        super().__init__(None)
        # n is the number of columns
        # m is the number of rows
        self.weight = Matrix(n=vocab_size,m=d_model)
        self.vocab_size, self.d_model = vocab_size, d_model

    def forward(self, token_ids: list[int]) -> Matrix:
        matrixNew = []
        for token_id in token_ids:
            matrixNew.append[self.weight.X[token_id]]
        return Matrix(matrix=matrixNew)
    
class PositionalEncoding(Object):
    def __init__(self, max_len: int, d_model: int):
        super().__init__(None)
        ## precompute pe[pos][i]
        self.pe = Matrix(m=max_len,n=d_model)        
        for pos in range(max_len):
            for i in range(0, d_model, 2):
                self.pe.X[pos][i]   = sin(pos / (10000 ** (i / d_model)))
                if i+1 < d_model:
                    self.pe.X[pos][i+1] = cos(pos / (10000 ** (i / d_model)))

    def forward(self, embeddings: Matrix) -> Matrix:
        ## add positional encoding to each time step
        returnMatrix = []
        for i in range(embeddings.m):
            row = []
            for j,e in enumerate(embeddings.X[i]):
                row.append(e+self.pe.X[i][j])
            returnMatrix.append(row)
        return Matrix(matrix=returnMatrix)

