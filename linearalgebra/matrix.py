class Matrix:
    def __init__(self,m:int,n:int):
        self.matrix = []
        self.m = m
        self.n = n
        for val1 in range(m):
            list = []
            for val2 in range(n):
                list.append(0)
            self.matrix.append(list)

    def returnMatrix(self):
        return self.matrix
    
    def matirxDimensions(self):
        return self.m, self.n
    
    def matrixAddition(self,matrix:'Matrix'):
        otherMatrixM, otherMatrixN = matrix.matirxDimensions()
        if self.m!=otherMatrixM or self.n!=otherMatrixN:
            raise ValueError("The two matrix sizes should be the same")
        resultMatrix = []
        for row in self.matrix:
            resultRow = []
            for column in self.matrix:
                resultRow.append(self.matrix[row][column]+matrix[row][column])
            resultMatrix.append(resultRow)

    def matrixMultiply(self):
        pass

    def matrixChainMultiply(self, listOfMatrix:list):
        self._verifyMatrixChain(listOfMatrix)

    def _verifyMatrixChain(self,listOfMatrix:list):
        for index in listOfMatrix:
            if not isinstance(listOfMatrix[index],'Matrix'):
                raise TypeError("Only two matrix can be combined")
            if index !=0:
                prev = index-1
                prevM,prevN = listOfMatrix[prev].matirxDimensions()
                currM,currN = listOfMatrix[index].matirxDimensions()
                if prevN!=currM:
                    raise ValueError("Matrix Dimensions prevents multiplication.")

    def matrixDetermineEigenValue(self):
        pass