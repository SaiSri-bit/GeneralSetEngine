import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# llm.py
from layers.embedding import TokenEmbedding, PositionalEncoding
from transformer import Transformer
from constants import random

class LLM:
    def __init__(self, vocab_size, max_len, num_layers, d_model, num_heads, d_ff):
        ## Add in the embedding layers
        self.tok_emb = TokenEmbedding(vocab_size, d_model)
        self.pos_emb = PositionalEncoding(max_len, d_model)
        ## Set up the Transformer Layer
        self.model   = Transformer(num_layers, d_model, num_heads, d_ff)
        # Have the final search preset up 
        self.final_W = [[0.01]*d_model for _ in range(vocab_size)]
        self.vocab_size = vocab_size

    def forward(self, token_ids):
        ## This class will just call the forward methods found in the previous layers
        x = self.tok_emb.forward(token_ids)
        x = self.pos_emb.forward(x)
        out = self.model.forward(x, x, src_mask=None, tgt_mask=self._causal_mask(len(x)))
        
        ## After that is done show the change on the vocabs logits
        return [
            [sum(out[t][u]*self.final_W[v][u] for u in range(len(out[0])))
             for v in range(self.vocab_size)]
            for t in range(len(out))
        ]

    def _causal_mask(self, seq_len):
        # This is a simple masking method
        return [[j <= i for j in range(seq_len)] for i in range(seq_len)]

    def generate(self, prompt_ids, max_new_tokens=20):
        ## Self explanitory, its the part that deals with initiating the things
        generated = prompt_ids[:]
        for _ in range(max_new_tokens):
            logits = self.forward(generated)
            next_token = self._sample(logits[-1])
            generated.append(next_token)
        return generated

    def _sample(self, logits):
        ## simple argmax or random‐top‐k, here argmax:
        return max(range(len(logits)), key=lambda i: logits[i])
