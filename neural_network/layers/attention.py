import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import sqrt
from neural_network.activation import softmax
from categories.matrix import Matrix, matrixMultiply

class ScaledDotProductAttention:
    def __init__(self):
        pass

    def forward(self, Q:Matrix, K:Matrix, V:Matrix, mask=None):
        # 1. compute scores = Q @ K^T / sqrt(d_k)
        d_k = Q.n
        K_t = Matrix(matrix=K.findTranspose())
        scores = Matrix(matrix=Q.X)
        scores.matrixMultiply(K_t)
        for i in range(scores.m):
            for j in range(scores.n):
                scores.X[i][j] = scores.X[i][j]/sqrt(d_k)

        # 2. apply mask (if provided)
        if mask:
            for i in range(scores.m):
                for j in range(scores.m):
                    if not mask[i][j]:
                        scores[i][j] = -1e9

        # 3. softmax the row
        attn = [softmax(row) for row in scores]

        # 4. weighted sum: attn @ V
        output = Matrix(matrix=attn)
        output.matrixMultiply(V) 
        return output

class MultiHeadAttention:
    def __init__(self, d_model: int, num_heads: int):
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        # initialize per-head linear projections as weight matrices
        self.Wq = [Matrix(m=d_model, n=d_model) for _ in range(num_heads)]
        self.Wk = [Matrix(m=d_model, n=d_model) for _ in range(num_heads)]
        self.Wv = [Matrix(m=d_model, n=d_model) for _ in range(num_heads)]
        self.Wo = Matrix(m=d_model, n=d_model)
        self.dot = ScaledDotProductAttention()

    def _linear(self, X:Matrix, W:Matrix):
        # X: list of T vectors (d_model), W: d_model×d_model
        return matrixMultiply(X,W)

    def forward(self, X:Matrix, mask=None):
        # 1. project X to Q,K,V for each head
        heads_output = []
        for h in range(self.num_heads):
            Q1 = self._linear(X, self.Wq[h])
            K1 = self._linear(X, self.Wk[h])
            V1 = self._linear(X, self.Wv[h])
            heads_out = self.dot.forward(Q1,K1,V1,mask)
            heads_output.append(heads_out)

        # 2. concatenate heads on last dim
        concat = []
        for row in range(len(heads_output[0].X)):
            concat_row = [] 
            for head in heads_output: 
                concat_row.extend(head.X[row]) 
            concat.append(concat_row)
        concat_matrix = Matrix(matrix=concat)

        # 3. final linear
        return self._linear(concat_matrix, self.Wo)
