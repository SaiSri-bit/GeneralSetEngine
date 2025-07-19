from .Category import Object

class Matrix(Object):
    def __init__(self,m:int=-1,n:int=-1,matrix:list=None,val=0):
        if m != -1 and n!=-1:
            matrix = []
            self.m = m
            self.n = n
            for val1 in range(m):
                row = []
                for val2 in range(n):
                    row.append(val)                        
                matrix.append(row)
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
            raise ValueError(f"An incorrect value for a matrix was given")
    
    def printMatrix(self):
        print(self.X)

    def returnMatrix(self):
        return self.X
    
    def matirxDimensions(self):
        return self.m, self.n
    
    def matrixAddition(self,matrix:'Matrix'):
        otherMatrixM, otherMatrixN = matrix.matirxDimensions()
        if self.m!=otherMatrixM or self.n!=otherMatrixN:
            raise ValueError("The two matrix sizes should be the same")
        resultMatrix = []
        for row in range(self.m):
            resultRow = []
            for column in range(self.n):
                resultRow.append(self.X[row][column]+matrix.X[row][column])
            resultMatrix.append(resultRow)
        self.X = resultMatrix

    def matrixMultiply(self,otherMatrix:'Matrix'):
        matrixChain = []
        matrixChain.append(Matrix(matrix=self.X))
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
        self.n = otherMatrix.n
    
    def deleteRow(self,index:int):
        self.X.pop(index)
        self.m = self.m-1
    
    def deleteColumn(self, index:int):
        for i in range(self.m):
            self.X[i].pop(index)
        self.n=self.n-1

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
    
    def findTranspose(self):
        transpose = []
        for column in range(self.n):
            row = []
            for val in range(self.m):
                row.append(self.X[val][column])
            transpose.append(row)
        return transpose 
    
    def row_echelon_form(self):
        newMatrix = self.X.copy()
        # Start from the left most column
        leadRow = 0
        for columnIndex in range(self.n):
            # Check to see if we have gone through the entire matrix, if so return the matrix
            if leadRow>=self.m: return Matrix(matrix=newMatrix)
            # Find the smallest nonzero value which will be used as pivot
            smallVal = 1999999
            pivot = -1
            for rowIndex in range(self.m):
                if rowIndex<leadRow:
                    continue
                if (newMatrix[rowIndex][columnIndex]<smallVal) and (abs(newMatrix[rowIndex][columnIndex])>0):
                    smallVal = newMatrix[rowIndex][columnIndex] # Store the value that we will be dealing with
                    pivot = rowIndex # Store the pivot row

            # If the entire column is all 0's we should just skip the column and move to the next column
            if pivot == -1:
                leadRow = leadRow+1
                continue

            # Check to see if the pivot is in the right position based on going down row by row
            # If it is not, swap the leadRow with the row that we are using as a pivot
            if leadRow!=pivot:
                currentRow = newMatrix[leadRow]
                pivotRow = newMatrix[pivot]
                newMatrix[leadRow]=pivotRow
                newMatrix[pivot]=currentRow
                pivot = leadRow

            # Algorithmically reduce the row such that the leading value is 1
            for pivotColumnIndex in range(self.n):
                newMatrix[pivot][pivotColumnIndex]=newMatrix[pivot][pivotColumnIndex]/smallVal
            
            for rowIndex in range(0,self.m):
                leadingVal = newMatrix[rowIndex][columnIndex]
                if (rowIndex == leadRow) or (abs(leadingVal) < 1e-12):
                    continue
                cloned = newMatrix[pivot].copy()
                for column in range(self.n):
                    cloned[column]= cloned[column]*leadingVal
                for column in range(self.n):
                    newMatrix[rowIndex][column]=newMatrix[rowIndex][column]-cloned[column]
            leadRow = leadRow+1

    def rank(self):
        ref = self.row_echelon_form()
        r = 0
        for row in ref.X:
            if any(abs(x) > 1e-10 for x in row):
                r=r+1
        return r
    
    def nullity(self):
        return self.n-self.rank()
    
    def kernal_basis(self):
        ref = self.row_echelon_form()
        pivot_col=[]
        for r in range(self.m):
            for c in range(self.n):
                if abs(ref.X[r][c])>1e-10:
                    pivot_col.append(c)
                    break
        free_vars=[]
        for c in range(self.n):
            if c not in pivot_col:
                free_vars.append(c)
        basis=[]
        for free_var in free_vars:
            vec=[0]*self.n
            vec[free_var]=1
            for r in range(self.m-1,-1,-1):
                row = ref.X[r]
                lead_index = next((c for c in range(self.n) if abs(row[c]) > 1e-10), None)
                if lead_index is not None and lead_index < free_var:
                    sum_val = sum(row[c] * vec[c] for c in range(lead_index + 1, self.n))
                    vec[lead_index] = -sum_val
            basis.append(vec)
        return basis
    


            

            
            


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
        if not isinstance(listOfMatrix[index],Matrix):
            raise TypeError("Only two matrix can be combined")
        if index !=0:
            prev = index-1
            prevM,prevN = listOfMatrix[prev].matirxDimensions()
            currM,currN = listOfMatrix[index].matirxDimensions()
            if prevN!=currM:
                raise ValueError(f'Matrix Dimensions prevents multiplication.{prevM}x{prevN} vs {currM}x{currN} ')

def importMatrix(path:str):
    with open(f'{path}', 'r') as f:
        newMatrix = []
        for line in f:
            row = []
            items = line.split(',')
            for item in items:
                row.append(item)
            newMatrix.append(row)
    return Matrix(matrix=newMatrix)