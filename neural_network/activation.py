from constants import exp, sin, cos, sqrt
## This file is similar to the constants file but it deals with the computations of activation
## Functions

#Softmax function
def softmax(x: list[float]) -> list[float]:
    exps = [exp(v) for v in x]
    s = sum(exps)
    return [v/s for v in exps]