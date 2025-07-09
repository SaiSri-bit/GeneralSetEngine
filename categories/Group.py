from .Set import Set, function
from .Category import Object,Morphism, Operation

# A Group as an object caan be viewed as a set followed with an operation that follow as a certain
# set of laws described below. To implement this, we should first define what an operation can be

        
class grp(Object):
    def __init__(self, elements:Set, identity, operation:Operation ):
        # Firstly, confirm that the identity element is part of the set
        if not (elements.contains(identity)):
            raise TypeError("Identity Element is missing from set")
        
        # Then store the appropariate variables
        self.X = elements.X # The set of elements is the main thing being stored
        self.operation = operation # Store the operation as another variable to be called later
        self.identity = identity # The identity element is one of the most important elements and should be stored seperately

        # After storing the above variables, we should also confirm whether or not the set and operation
        # will form a group by making sure the definition of the groups are met. 
        if not self.verify_group(identity):
            raise TypeError ("One of the verifications failed. Set and Operation do not form group")


    def verify_group(self,identity):
        # There are 4 main criteria that a set and operation pair have to meet to be considered to be a group:
        # 1. The set must be closed (the operation can only transmute one element of the set to another element 
        # that is in that same set)
        # 2. The operation must be associative (a*b)*c = a*(b*c)
        # 3. The set must contain a unique identity element such that a*e = a
        # 4. The set must contain a unque inverse element such taht a*a^{-1}= e
        return self.verify_associative() and self.verify_identity(identity) and self.verify_inverse(identity) and self.verify_closed()
    

    def verify_associative(self):
        # This method parses through every possible three element combination and makes sure that associativity
        # is kept within the group with the operation
        for element1 in self.X:
            for element2 in self.X:
                for element3 in self.X:
                    if self.operation.apply(self.operation.apply(element1,element2),element3) != self.operation.apply(element1,self.operation.apply(element2,element3)):
                        print("Failed Associative")
                        return False 
        return True


    def verify_identity(self,identity):
        # This just goes ahead and insures that the element when operated with itself and the identity element
        # results in the starting element for all elements in the set
        for element in self.X:
            if not (self.operation.apply(element, identity) == element and self.operation.apply(identity, element) == element):
                print("Failed Identity")
                return False
        return True
    

    def verify_inverse(self,identity):
        # This method goes through every element, and makes sure that there exists some valid element such that
        # when both elements are combined under the given operation, the identity element is achieved
        for element1 in self.X:
            check = False
            count = 0
            while not check:
                if count == len(self.X):
                    print("Failed Inverse")
                    return False
                if self.operation.apply(element1,self.X[count]) == identity:
                    check = True
                count = count + 1 
        return True


    def verify_closed(self):
        # This method insures that all possible combinations of elements under the given operation will result
        # in another element that is within the existing set
        for a in self.X:
            for b in self.X:
                if self.operation.apply(a, b) not in self.X:
                    print(f"Failed Closure: {self.operation.apply(a, b)}")
                    return False
        return True
    

    def getIdentity(self):
        # We stored the identity earlier for a faster return
        return self.identity


    def find_Inverse(self,element):
        # Similar to verification, we just need go through each combinations of elements until one combines
        # to the identity element at which point we return that intitial element
        check = False
        count = 0
        while not check:
            if self.operation.apply(element,self.X[count]) == self.identity:
                break
            count = count + 1 
            if count == len(self.X):
                return False
                

    def check_if_abeliean(self):
        # Abelian groups are groups that have a fifth property of commutativity and the method checks and
        # returns true or false based on if its abelian or not.
        for element1 in self.X:
            for element2 in self.X:
                if self.operation.apply(element1,element2) != self.operation.apply(element2,element1):
                    return False 
        return True
    
    def returnObject(self):
        object = []
        object.append(self.X)
        object.append(self.operation)
        return object

class grpHomomorphism(Morphism):
    pass

