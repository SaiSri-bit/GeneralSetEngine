from categories.Category import Object
from constants import sin,cos

class TokenEmbedding(Object):
    def __init__(self, vocab_size: int, d_model: int):
        super().__init__(None)
        self.weight = [[(i + j) * 0.01 for j in range(d_model)]
                       for i in range(vocab_size)]
        self.vocab_size, self.d_model = vocab_size, d_model

    def forward(self, token_ids: list[int]) -> list[list[float]]:
        return [self.weight[token_id] for token_id in token_ids]
    
class PositionalEncoding(Object):
    def __init__(self, max_len: int, d_model: int):
        super().__init__(None)
        ## precompute pe[pos][i]
        self.pe = [[0]*d_model for _ in range(max_len)]
        for pos in range(max_len):
            for i in range(0, d_model, 2):
                self.pe[pos][i]   = sin(pos / (10000 ** (i / d_model)))
                if i+1 < d_model:
                    self.pe[pos][i+1] = cos(pos / (10000 ** (i / d_model)))

    def forward(self, embeddings: list[list[float]]) -> list[list[float]]:
        ## add positional encoding to each time step
        return [
            [e + self.pe[i][j] for j, e in enumerate(embeddings[i])]
            for i in range(len(embeddings))
        ]
