from Category import Object,Morphism

class Set(Object):
    def __init__(self, X:list):
        if self._contains_non_number_(X):
            raise ValueError("Invalid Array, contains Full Strings. Please Use other characters")
        super().__init__(X)

    def _contains_non_number_(self,lst):
        if len(lst)==0:
            return False
        for element in lst:
            if not isinstance(element, (int, float, complex,list, Set)):
                return True
            if isinstance(str):
                if len(element)>1:
                    return True
        return False
    
    def getSet(self):
        return self.X
    
    def getPowerSet(self):
        n = len(self.X)
        powerset = []
        for i in range(2 ** n):  
            subset = []
            for j in range(n):  
                if (i & (1 << j)) != 0:
                    subset.append(self.X[j])
            powerset.append(subset)
        return powerset

    def contains(self, element):
        return element in self.X
    
    def is_subset(self, Y):
        if not isinstance(Y, set):
            raise TypeError("Argument must be an instance of Set.")
        return Set(self.X).issubset(set(Y.getSet()))

    def is_superset(self, Y):
        if not isinstance(Y, set):
            raise TypeError("Argument must be an instance of Set.")
        return Set(self.X).issuperset(Y.getSet())

    def is_equal(self, Y):
        if not isinstance(Y, set):
            raise TypeError("Argument must be an instance of Set.")
        return set(self.X) == set(Y.getSet())

    def union(self, Y):
        if not isinstance(Y, set):
            raise TypeError("Argument must be an instance of Set.")
        return Set(list(set(self.X).union(set(Y.getSet()))))
    
    def intersection(self, Y):
        if not isinstance(Y, set):
            raise TypeError("Argument must be an instance of Set.")
        return Set(list(set(self.X).intersection(set(Y.getSet()))))
    

class function(Morphism):
    def __init__(self, map:dict):
        self.map = map
        self.domain = map.keys()
        self.codomain = map.items()

    def validDomainSet(self, domain:Set):
        for element in domain:
            if element not in self.domain:
                return False
        return True
    
    def validCoDomainSet(self, CoDomain:Set):
        for element in CoDomain:
            if element not in self.codomain:
                return False
        return True
    
    def validateFunction(self):
        if len(self.codomain)==len(set(self.codomain)):
            return True
        return False