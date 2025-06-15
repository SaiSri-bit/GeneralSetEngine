class Object:
    def __init__(self,X):
        self.X = X

class Morphism:
    def __init__(self, domain, codomain):
        self.domain = domain  
        self.codomain = codomain

class Category:
    def __init__(self, X:Object, Y:Object, f:Morphism):
        self.X = X
        self.Y = Y
        self.f = f

class IdentityMorphism(Morphism):
    def __init__(self, obj):
        super().__init__(obj, obj) 

class Functors (Morphism):
    def forget(self):
        pass
