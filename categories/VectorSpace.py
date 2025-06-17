from Set import Set, function
import random

class vectk(object):
    def __init__(self,elements:Set,additiveIdentity:tuple):
        self.X = elements
        self.aidentity = additiveIdentity
        self.midentity = 1
        if not self.verify():
            raise ValueError("Vector Space cannot be created due to not meeting criteria")
    
    def verify(self):
        self.verifyIdentity() and self.verifyInverse() and self.verifyCommutative() and self.verifyAssociativity() and self.verifyDistribution() and self.verifyScalarFieldMultiplication()
    
    def verifyIdentity(self):
        for vector in self.X:
            if self.vectorAddition(vector,self.aidentity) != vector:
                return False
            if self.scalarVectorMultiplication(vector,self.midentity) != vector:
                return False

    def verifyInverse(self):
        for vector1 in self.X:
            check = False
            count = 0 
            while not check:
                if count == len(self.X):
                    return False
                if self.vectorAddition(vector1,self.X[count]) == self.aidentity:
                    check = True
                count = count+1
        return True
    
    def verifyCommutative(self):
        for vector1 in self.X:
            for vector2 in self.X:
                if self.vectorAddition(vector1,vector2)!=self.vectorAddition(vector2,vector1):
                    return False
        return True

    def verifyAssociativity(self):
        for vector1 in self.X:
            for vector2 in self.X:
                for vector3 in self.X:
                    vectorsum1 = self.vectorAddition(vector1,self.vectorAddition(vector2,vector3))
                    vectorsum2 = self.vectorAddition(self.vectorAddition(vector1,vector2,),vector3)
                    if vectorsum1!=vectorsum2:
                        return False
        return True
    
    def verifyScalarFieldMultiplication(self):
        for vector in self.X:
            scalar1 = random.randrange(100)
            scalar2 = random.randrange(100)
            product = scalar1*scalar2
            if self.scalarVectorMultiplication(vector,product) != self.scalarVectorMultiplication(self.scalarVectorMultiplication(vector,scalar1),scalar2):
                return False
        return True
    
    def verifyDistribution(self):
        return self.verifyScalarDistribution() and self.verifyRegularDistribution
    
    def verifyScalarDistribution(self):
        for vector in self.X:
            scalar1 = random.randrange(100)
            scalar2 = random.randrange(100)
            summation = scalar1+scalar2
            if self.scalarVectorMultiplication(vector,summation) != self.vectorAddition(self.scalarVectorMultiplication(vector,scalar1),self.scalarVectorMultiplication(vector,scalar2)):
                return False
        return True
    
    def verifyRegularDistribution(self):
        for vector1 in self.X:
            for vector2 in self.X:
                scalar = random.randrange(100)
                sumofvectors = self.vectorAddition(vector1,vector2)
                firstvectorproduct= self.scalarVectorMultiplication(scalar,vector1)
                secondvectorproduct= self.scalarVectorMultiplication(scalar,vector2)
                sumofvectorspost = self.vectorAddition(firstvectorproduct,secondvectorproduct)
                if self.scalarVectorMultiplication(scalar,sumofvectors)!=sumofvectorspost:
                    return False
        return True

    def vectorAddition(self,vector1:tuple,vector2:tuple):
        if len(vector1)!=len(vector2):
            raise ValueError("Vectors cannot be combined as the size are not equal")
        resultvector = []
        for index in range(len(vector1)):
            resultvector.append(vector1[index]+vector2[index])
        return tuple(resultvector)
    
    def scalarVectorMultiplication(self,vector1:tuple,scalar1):
        resultvector = []
        for index in range(len(vector1)):
            resultvector.append(vector1[index]*scalar1)
        return resultvector
    
class linearMaps(function):
    pass