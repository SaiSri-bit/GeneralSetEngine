from .Set import Set, function
from .Category import Object, Operation
from .TopologicalSpace import continuousFunction

class met(object):
    def __init__(self, elements:list, distFunc:Operation, distances:dict):
        self.X = elements
        self.distanceOperation = distFunc
        self.distances = distances
        if not self.verifyDistance():
            return TypeError("Distance function is invalid")
        
    def verifyDistance(self):
        for element1 in self.X:
            for element2 in self.X:
                if self.distances.get([element1,element2])!= self.distanceOperation.apply(element1,element2):
                    return False
        return True