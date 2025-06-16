from Set import Set, function


class vectk(object):
    def __init__(self,elements:Set,additiveIdentity:tuple):
        self.X = elements
        self.aidentity = additiveIdentity
        self.midentity = 1
        if not self.verify():
            raise ValueError("Vector Space cannot be created due to not meeting criteria")
    def verify(self):
        self.verifyIdentity() and self.verifyInverse() and self.verifyCommutative() and self.verifyAssociativity() and self.verifyDistribution()
    def verifyIdentity(self):
        for vector in self.X:
            if self.vectorAddition(vector,self.aidentity) != vector:
                return False
            if self.scalarVectorMultiplication(vector,self.midentity) != vector:
                return False
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