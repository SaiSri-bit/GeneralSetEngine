# transformer.py
from layers.attention import MultiHeadAttention
from constants import sqrt
def layer_norm(x):
    ## very bare bones (no learnable γ, β)
    mean = sum(x)/len(x)
    var  = sum((xi-mean)**2 for xi in x)/len(x)
    return [(xi-mean)/sqrt(var+1e-5) for xi in x]

class FeedForward:
    def __init__(self, d_model, d_ff):
        ## two linear layers: W1: d_model→d_ff, W2: d_ff→d_model
        self.W1 = [[0.01]*d_model for _ in range(d_ff)]
        self.W2 = [[0.01]*d_ff   for _ in range(d_model)]

    def forward(self, x_seq):
        ## x_seq: list of T vectors (d_model)
        hidden = [[sum(x_seq[t][u]*self.W1[v][u] for u in range(len(x_seq[0])))
                   for v in range(len(self.W1))]
                  for t in range(len(x_seq))]
        ## apply ReLU
        hidden = [[max(0,h) for h in row] for row in hidden]
        ## back to d_model
        return [[sum(hidden[t][u]*self.W2[v][u] for u in range(len(hidden[0])))
                 for v in range(len(self.W2))]
                for t in range(len(hidden))]

class EncoderLayer:
    def __init__(self, d_model, num_heads, d_ff):
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ff        = FeedForward(d_model, d_ff)

    def forward(self, x_seq, mask=None):
        # Self‐attention + add & norm
        attn_out = self.self_attn.forward(x_seq, mask)
        x_seq = [layer_norm([x_seq[t][i] + attn_out[t][i]
                             for i in range(len(x_seq[0]))])
                 for t in range(len(x_seq))]
        # Feed‐forward + add & norm
        ff_out  = self.ff.forward(x_seq)
        return [layer_norm([x_seq[t][i] + ff_out[t][i]
                            for i in range(len(x_seq[0]))])
                for t in range(len(x_seq))]

class DecoderLayer:
    def __init__(self, d_model, num_heads, d_ff):
        self.self_attn   = MultiHeadAttention(d_model, num_heads)
        self.cross_attn  = MultiHeadAttention(d_model, num_heads)
        self.ff          = FeedForward(d_model, d_ff)

    def forward(self, tgt_seq, enc_seq, tgt_mask=None, memory_mask=None):
        # Masked self-attn
        m1 = self.self_attn.forward(tgt_seq, tgt_mask)
        tgt_seq = [layer_norm([tgt_seq[t][i] + m1[t][i] for i in range(len(tgt_seq[0]))])
                   for t in range(len(tgt_seq))]
        # Cross‐attention
        m2 = self.cross_attn.forward(tgt_seq + enc_seq, memory_mask)
        tgt_seq = [layer_norm([tgt_seq[t][i] + m2[t][i] for i in range(len(tgt_seq[0]))])
                   for t in range(len(tgt_seq))]
        # Feed-forward
        ff = self.ff.forward(tgt_seq)
        return [layer_norm([tgt_seq[t][i] + ff[t][i] for i in range(len(tgt_seq[0]))])
                for t in range(len(tgt_seq))]

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
