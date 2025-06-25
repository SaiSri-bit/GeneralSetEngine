import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import sqrt
from neural_network.activation import softmax
from categories.matrix import Matrix

class ScaledDotProductAttention:
    def __init__(self):
        pass

    def forward(self, Q, K, V, mask=None):
        """
        Q, K, V: each is a list of T vectors of dimension d_k
        mask: optional list of lists to mask out future positions
        returns: list of T output vectors
        """
        # 1. compute scores = Q @ K^T / sqrt(d_k)
        d_k = len(Q[0])
        scores = [
            [
                sum(Q[i][u]*K[j][u] for u in range(d_k)) / sqrt(d_k)
                for j in range(len(K))
            ]
            for i in range(len(Q))
        ]
        # 2. apply mask (if provided)
        if mask:
            for i in range(len(scores)):
                for j in range(len(scores)):
                    if not mask[i][j]:
                        scores[i][j] = -1e9
        # 3. softmax
        attn = [softmax(row) for row in scores]
        # 4. weighted sum: attn @ V
        output = [
            [
                sum(attn[i][j] * V[j][k] for j in range(len(V)))
                for k in range(len(V[0]))
            ]
            for i in range(len(attn))
        ]
        return output

class MultiHeadAttention:
    def __init__(self, d_model: int, num_heads: int):
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        # initialize per-head linear projections as weight matrices
        self.Wq = [[[0.01]*(d_model) for _ in range(d_model)] for _ in range(num_heads)]
        self.Wk = [[[0.01]*(d_model) for _ in range(d_model)] for _ in range(num_heads)]
        self.Wv = [[[0.01]*(d_model) for _ in range(d_model)] for _ in range(num_heads)]
        self.Wo = [[(i+j)*0.01 for j in range(d_model)] for i in range(d_model)]
        self.dot = ScaledDotProductAttention()

    def _linear(self, X, W):
        # X: list of T vectors (d_model), W: d_model×d_model
        return [
            [sum(X[t][u] * W[u][v] for u in range(len(W))) for v in range(len(W[0]))]
            for t in range(len(X))
        ]

    def forward(self, X, mask=None):
        # 1. project X to Q,K,V for each head
        heads_output = []
        for h in range(self.num_heads):
            Q = self._linear(X, self.Wq[h])
            K = self._linear(X, self.Wk[h])
            V = self._linear(X, self.Wv[h])
            heads_output.append(self.dot.forward(Q, K, V, mask))
        # 2. concatenate heads on last dim
        concat = [
            sum((heads_output[h][t] for h in range(self.num_heads)), [])
            for t in range(len(X))
        ]
        # 3. final linear
        return self._linear(concat, self.Wo)
