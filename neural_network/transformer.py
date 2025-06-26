import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from categories.matrix import Matrix, matrixMultiply
from neural_network.activation import ReLU
from layers.attention import MultiHeadAttention
from constants import sqrt



def layer_norm(x):
    ## very bare bones (no learnable γ, β)
    mean = sum(x) / len(x)
    var = sum((xi - mean) ** 2 for xi in x) / len(x)
    row = [(xi - mean) / sqrt(var + 1e-5) for xi in x]
    return row


class FeedForward:
    def __init__(self, d_model, d_ff):
        ## two linear layers: W1: d_model→d_ff, W2: d_ff→d_model
        self.W1 = Matrix(m=d_model,n=d_ff,val=0.01)
        self.W2 = Matrix(m=d_ff,n=d_model,val=0.01)
        # self.W1 = [[0.01]*d_model for _ in range(d_ff)]
        # self.W2 = [[0.01]*d_ff   for _ in range(d_model)]

    def forward(self, x_seq:Matrix):
        ## x_seq: list of T vectors (d_model)
        hidden = Matrix(matrix=matrixMultiply(x_seq,self.W1))

        # hidden = [[sum(x_seq[t][u]*self.W1[v][u] for u in range(len(x_seq[0])))
        #            for v in range(len(self.W1))]
        #           for t in range(len(x_seq))]

        ## apply ReLU
        for row in range(x_seq.m):
            hidden.X[row] = ReLU(hidden.X[row])

        ## back to d_model
        return Matrix(matrix=matrixMultiply(hidden,self.W2))

        
        # return [[sum(hidden[t][u]*self.W2[v][u] for u in range(len(hidden[0])))
        #          for v in range(len(self.W2))]
        #         for t in range(len(hidden))]

class EncoderLayer:
    def __init__(self, d_model, num_heads, d_ff):
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ff        = FeedForward(d_model, d_ff)

    def forward(self, x_seq:Matrix, mask=None):
        # Self‐attention + add & norm
        attn_out = self.self_attn.forward(x_seq, mask)
        added_matrix = Matrix(matrix=attn_out.X)
        added_matrix.matrixAddition(x_seq)
        normailze_matrix = []
        for row in range(added_matrix.m):
            normailze_matrix.append(layer_norm(row))
        x_seq = Matrix(matrix=normailze_matrix)
        ff_out = self.ff.forward(x_seq)
        return ff_out.matrixAddition(x_seq)
        # added_matrix = Matrix(matrix=[
        #     [x_seq.X[t][i] + attn_out.X[t][i] for i in range(x_seq.n)]
        #     for t in range(x_seq.m)
        # ])

        # Apply layer normalization to each row
        # normalized_matrix = Matrix(matrix=[
        #     layer_norm(row) for row in added_matrix.X
        # ])

        # Update x_seq
        # x_seq = normalized_matrix

        # Feed‐forward + add & norm
        # ff_out  = self.ff.forward(x_seq)
        # return [layer_norm([x_seq[t][i] + ff_out[t][i]
        #                     for i in range(len(x_seq[0]))])
        #         for t in range(len(x_seq))]

class DecoderLayer:
    def __init__(self, d_model, num_heads, d_ff):
        self.self_attn   = MultiHeadAttention(d_model, num_heads)
        self.cross_attn  = MultiHeadAttention(d_model, num_heads)
        self.ff          = FeedForward(d_model, d_ff)

    def forward(self, tgt_seq:Matrix, enc_seq:Matrix, tgt_mask=None, memory_mask=None):
        # Masked self-attn
        added_matrix = self.self_attn.forward(tgt_seq, tgt_mask)
        added_matrix.matrixAddition(tgt_seq)

        normalizeMatrix = []
        for row in range(added_matrix.m):
            normalizeMatrix.append(layer_norm(added_matrix.X[row]))

        tgt_seq = Matrix(matrix=normalizeMatrix)
        
        # Cross-attnetion
        tgt_seq_and_enc_seq = tgt_seq
        tgt_seq_and_enc_seq.matrixAddition(enc_seq)
        added_matrixM2 = self.cross_attn.forward(tgt_seq_and_enc_seq, memory_mask)
        added_matrixM2.matrixAddition(tgt_seq)
        normalizeMatrix=[]
        for row in range(added_matrixM2.m):
            normalizeMatrix.append(layer_norm(added_matrixM2.X[row]))
        tgt_seq = Matrix(matrix=normalizeMatrix)

        # Feed Forward
        ff = self.ff.forward(tgt_seq)
        tgt_seq.matrixAddition(ff)
        normalizeMatrix = []
        for row in range(tgt_seq.m):
            normalizeMatrix.append(tgt_seq.X[row])
        return Matrix(matrix=normalizeMatrix)




        # tgt_seq = [layer_norm([tgt_seq[t][i] + m1[t][i] for i in range(len(tgt_seq[0]))])
        #            for t in range(len(tgt_seq))]
        # Cross‐attention
        # m2 = self.cross_attn.forward(tgt_seq + enc_seq, memory_mask)
        # tgt_seq = [layer_norm([tgt_seq[t][i] + m2[t][i] for i in range(len(tgt_seq[0]))])
        #            for t in range(len(tgt_seq))]
        # Feed-forward
        # ff = self.ff.forward(tgt_seq)
        # return [layer_norm([tgt_seq[t][i] + ff[t][i] for i in range(len(tgt_seq[0]))])
        #         for t in range(len(tgt_seq))]

class Transformer:
    def __init__(self, num_layers, d_model, num_heads, d_ff):
        self.enc_layers = [EncoderLayer(d_model, num_heads, d_ff)
                           for _ in range(num_layers)]
        self.dec_layers = [DecoderLayer(d_model, num_heads, d_ff)
                           for _ in range(num_layers)]

    def encode(self, src, src_mask=None):
        x = src
        for layer in self.enc_layers:
            x = layer.forward(x, src_mask)
        return x

    def decode(self, tgt, memory, tgt_mask=None, memory_mask=None):
        y = tgt
        for layer in self.dec_layers:
            y = layer.forward(y, memory, tgt_mask, memory_mask)
        return y

    def forward(self, src, tgt, src_mask=None, tgt_mask=None, memory_mask=None):
        memory = self.encode(src, src_mask)
        return self.decode(tgt, memory, tgt_mask, memory_mask)
