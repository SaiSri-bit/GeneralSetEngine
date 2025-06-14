from Set import Set, function
from Category import Object,Morphism

class Operation:
    def __init__(self, op_func):
        if not callable(op_func):
            raise TypeError("Operation must be a callable function.")
        self.op_func = op_func

    def apply(self, a, b):
        return self.op_func(a, b)

        
class grp(Object):
    def __init__(self, elements:Set, identity, operation:Operation ):
        self.X = elements
        self.operation = operation
        if not (elements.contains(identity)):
            raise TypeError("Identity Element is missing from set")
        if not self.verify_group(identity):
            raise TypeError ("One of the verifications failed. Set and Operation do not form group")
        self.identity = identity


    def verify_group(self,identity):
        return self.verify_associative() and self.verify_identity(identity) and self.verify_inverse(identity) and self.verify_closed()
    

    def verify_associative(self):
        for element1 in self.X:
            for element2 in self.X:
                for element3 in self.X:
                    if self.operation.apply(self.operation.apply(element1,element2),element3) != self.operation.apply(element1,self.operation.apply(element2,element3)):
                        return False 
        return True


    def verify_identity(self,identity):
        for element in self.X:
            if not (self.operation.apply(element, identity) == element and self.operation.apply(identity, element) == element):
                return False
        return True
    

    def verify_inverse(self,identity):
        for element1 in self.X:
            check = False
            count = 0
            while not check:
                if self.operation.apply(element1,self.X[count]) == identity:
                    break
                count = count + 1 
                if count == len(self.X):
                    return False


    def verify_closed(self):
        for a in self.X:
            for b in self.X:
                if self.operation.apply(a, b) not in self.X:
                    return False
        return True
    

    def getIdentity(self):
        return self.identity


    def find_Inverse(self,element):
        check = False
        count = 0
        while not check:
            if self.operation.apply(element,self.X[count]) == self.identity:
                break
            count = count + 1 
            if count == len(self.X):
                return False
                

    def check_if_abeliean(self):
        for element1 in self.X:
            for element2 in self.X:
                if self.operation.apply(element1,element2) != self.operation.apply(element2,element1):
                    return False 
        return True

class grpHomomorphism(Morphism):
    pass

