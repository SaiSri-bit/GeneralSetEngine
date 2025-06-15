from Category import Object
from Set import Set
from Group import grp,grpHomomorphism, Operation

class ring(Object):
    def __init__(self, elements:Set, identity, operation1:Operation, operation2:Operation):
        self.X = elements
        self.identity = identity
        self.operation1 = operation1
        self.operation2 = operation2
        if not self.verifyRing():
            raise TypeError("Ring Criteria note met")
        
    def verifyRing(self):
        try:
            verifyIsGroup = grp(self.X,self.identity,self.operation1)
        except:
            raise TypeError("Ring does not meet Group Criteria")
        return verifyIsGroup.check_if_abeliean() and self.verifyDistribute() and self.verify_associative()
    
    def verifyDistribute(self):
        for element1 in self.X:
            for element2 in self.X:
                for element3 in self.X:
                    ls = self.operation2.apply(element1,self.operation1.apply(element2,element3))
                    rs = self.operation1(self.operation2(element1,element2),self.operation2(element1,element3))
                    if ls != rs:
                        return False
        return True
    def verify_associative(self):
        for element1 in self.X:
            for element2 in self.X:
                for element3 in self.X:
                    if self.operation2.apply(self.operation2.apply(element1,element2),element3) != self.operation2.apply(element1,self.operation2.apply(element2,element3)):
                        return False 
        return True  



class ringHomomorphism(grpHomomorphism):
    pass