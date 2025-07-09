# The basic units of a category is an object and morphism. Objects are essentially any mathematical
# structure or space. This is the basic foundational unit that will be extended by all other main
# objects. One important thing to note is that most class are a set with another feature. Rather
# than extending set, the object class will be extended and the set will be treated as a composition
# this allows to view both of them seperately and extend potential features of Objects.
class Object:
    def __init__(self,X):
        self.X = X
    def returnObject(self):
        return self.X

# Morphisms are essentially maps from one set of objects to another set of objects
class Morphism:
    def __init__(self, map:dict):
        self.map = map
        self.domain = map.keys()
        self.codomain = map.items()

# Categories are essentially like what was mentioned with morphism. There are sets of objects and 
# then a map from the two. This is very similar to morphisms but isnt directly the same. This is because
# the Category will be restricting the domain and codomain based on the two given objects rather
# than the exact morphism itself.
class Category:
    def __init__(self, X:Object, Y:Object, f:Morphism):
        self.X = X
        self.Y = Y
        self.f = f

class IdentityMorphism(Morphism):
    def __init__(self, obj):
        super().__init__(obj, obj) 

# Functors are specific morphisms that convert from one type of category to another type of category
class Functors (Morphism):
    def forget(self):
        pass

class Operation:
    # For the case of simplicity, any operations should be a callable function. This will allow
    # us to be able to conduct operations within the group
    def __init__(self, op_func):
        if not callable(op_func):
            raise TypeError("Operation must be a callable function.")
        self.op_func = op_func

    def apply(self, a, b):
        return self.op_func(a, b)