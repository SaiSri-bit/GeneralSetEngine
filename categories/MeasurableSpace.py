from .Set import Set, function
from .Category import Object,Morphism

class meas(Object):
    def __init__(self, elements:Set, sigma_algebra:list[list]):
        self.X = elements.X
        self.sigma_algebra = sigma_algebra
        self.verifySigma_Algebra()

    def verifySigma_Algebra(self):
        # Check to make sure that the empty set is within the sigma algebra
        if [] not in self.sigma_algebra:
            print ("Empty Set not in sigma algebra")
            return False
        
        # Check to see the entire underlying set is in the sigma algebra
        if [].append(self.X) not in self.sigma_algebra:
            print ("Underlying set is not within the sigma algebra")
            return False

        # Check to see if the sigma algebra contains the complement element for all elements with in
        # the sigma algebra
        for subset in self.sigma_algebra:
            complement = list(set(self.X).difference(set(subset)))
            if complement not in self.sigma_algebra:
                print(f"Sigma-algebra is not closed under complement: {subset}")
                return False

        # Check to see if there is closure under countable unions. One issue with the offered method
        # only checks with pair wise unions and not all possible combinations. The reason this implementation
        # is being used is that the actual computation. Therefore, it is heavyily reccomended checking
        # this particular property.
        for i, subset_a in enumerate(self.sigma_algebra):
            for subset_b in self.sigma_algebra[i:]:
                union = list(set(subset_a).union(set(subset_b)))
                if union not in self.sigma_algebra:
                    print(f"Sigma-algebra is not closed under union: {subset_a} and {subset_b}")
                    return False

        return True

    def returnObject(self):
        object = []
        object.append(self.X)
        object.append(self.sigma_algebra)
        return object

class measure(function):
    def __init__(self, map):
        super().__init__(map)
    def apply(self):
        pass

class measurableFunction(Morphism):
    pass