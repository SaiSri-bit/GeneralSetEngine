from .Category import Object

class Matrix(Object):
    def __init__(self,m:int=-1,n:int=-1,matrix:list=None):
        if m != -1 and n!=-1:
            matrix = []
            self.m = m
            self.n = n
            for val1 in range(m):
                list = []
                for val2 in range(n):
                    list.append(0)
                matrix.append(list)
            self.X = matrix
        elif (matrix!=None):
            size = 0
            index = 0
            for item in matrix:
                if not isinstance(item,list):
                    raise TypeError("Matrix Not provided")
                if index==0:
                    size = len(item)
                else:
                    if size!=len(item):
                        raise ValueError("Rows are not of the same length, buffer them first")
                index = index+1
            self.X = matrix
            self.m = len(matrix)
            self.n = len(matrix[0])
        else:
            raise ValueError(f"An incorrect value for a matrix was given {m},{n},{matrix}")

    def returnMatrix(self):
        return self.X
    
    def matirxDimensions(self):
        return self.m, self.n
    
    def matrixAddition(self,matrix:'Matrix'):
        otherMatrixM, otherMatrixN = matrix.matirxDimensions()
        if self.m!=otherMatrixM or self.n!=otherMatrixN:
            raise ValueError("The two matrix sizes should be the same")
        resultMatrix = []
        for row in self.X:
            resultRow = []
            for column in self.X[row]:
                resultRow.append(self.X[row][column]+matrix[row][column])
            resultMatrix.append(resultRow)
        self.X = resultMatrix

    def matrixMultiply(self,otherMatrix:'Matrix'):
        matrixChain = []
        matrixChain.append(self.X)
        matrixChain.append(otherMatrix)
        verifyMatrixChain(matrixChain)
        resultMatrix = []
        for i in range(self.m):
            new_row = []
            for j in range(otherMatrix.n):
                new_row.append(0)
            resultMatrix.append(new_row)
        for i in range(self.m):
            for j in range(otherMatrix.n):
                for k in range(self.n):
                    resultMatrix[i][j] += self.X[i][k] * otherMatrix.X[k][j]
        self.X = resultMatrix

    def qrDecompose(self):
        Q = []
        for _ in range(self.m):
            row = []
            for _ in range(self.n):
                row.append(0)
            Q.append(row)
        R = []
        for _ in range(self.n):
            row = []
            for _ in range(self.n):
                row.append(0)
            R.append(row)
        for j in range(self.n):
            v = [self.X[i][j] for i in range(self.m)] 
            for i in range(j):
                proj = sum([Q[k][i] * v[k] for k in range(self.m)])
                for k in range(self.m):
                    v[k] -= proj * Q[k][i]
            norm = sum([v[i] ** 2 for i in range(self.m)]) ** 0.5
            for i in range(self.m):
                Q[i][j] = v[i] / norm
            for i in range(j, self.n):
                R[j][i] = sum([Q[k][j] * self.X[k][i] for k in range(self.m)])
        return Matrix(Q), Matrix(R)  

    def matrixSolveEigenvalue(self,max_iter=1000, tol=1e-10):
        A = self.X
        for _ in range(max_iter):
            Q, R = self.qrDecompose()
            A_next = R.matrixMultiply(Q)
            diff = [[A[i][j] - A_next[i][j] for j in range(self.n)] for i in range(self.m)]
            diff_norm = sum([sum([x ** 2 for x in row]) for row in diff]) ** 0.5
            if diff_norm < tol:
                break
            A = A_next.X 
        eigenvalues = [A[i][i] for i in range(self.m)]
        return eigenvalues





## List of Methods that are related to two matrix without having to first create a matrix object
## This allows for combinations of Matrix objects without having to rewrite one or the other
def matrixMultiply(firstMatrix:'Matrix',otherMatrix:'Matrix'):
    matrixChain = []
    matrixChain.append(firstMatrix)
    matrixChain.append(otherMatrix)
    verifyMatrixChain(matrixChain)
    resultMatrix = []
    for i in range(firstMatrix.m):
        new_row = []
        for j in range(otherMatrix.n):
            new_row.append(0)
        resultMatrix.append(new_row)
    for i in range(firstMatrix.m):
        for j in range(otherMatrix.n):
            for k in range(firstMatrix.n):
                resultMatrix[i][j] += firstMatrix.X[i][k] * otherMatrix.X[k][j]
    return resultMatrix

    
def matrixChainMultiply(listOfMatrix:list):
    verifyMatrixChain(listOfMatrix)
    result = listOfMatrix[0]
    for index in range(len(listOfMatrix)):
        if index !=0:
            result = matrixMultiply(result,listOfMatrix[index])
    return result


def verifyMatrixChain(listOfMatrix:list):
    for index in range(len(listOfMatrix)):
        if not isinstance(listOfMatrix[index],'Matrix'):
            raise TypeError("Only two matrix can be combined")
        if index !=0:
            prev = index-1
            prevM,prevN = listOfMatrix[prev].matirxDimensions()
            currM,currN = listOfMatrix[index].matirxDimensions()
            if prevN!=currM:
                raise ValueError("Matrix Dimensions prevents multiplication.")

