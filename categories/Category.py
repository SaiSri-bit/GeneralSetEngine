class Category:
    def __init__(self, X, Y, f):
        self.X:Object = X
        self.Y:Object = Y
        self.f = f

class Object:
    def __init__(self,X):
        self.X = X

class Morphism:
    def __init__(self, domain, codomain):
        self.domain = domain  
        self.codomain = codomain

class IdentityMorphism(Morphism):
    def __init__(self, obj):
        super().__init__(obj, obj) 

class Functors (Morphism):
    def forget(self):
        pass
