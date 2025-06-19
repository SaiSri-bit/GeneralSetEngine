from categories.Category import Object
import matrix
class tensor(Object):
    def __init__(self):
        self.X = matrix(2,2)
    def __init__(self,tensor:list):
        if not self.verifyTensor():
            raise TypeError("Tensor was not provided")
        self.X = tensor