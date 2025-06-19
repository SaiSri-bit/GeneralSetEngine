from .Set import Set, function
from .Category import Object
class top(Object):
    def __init__(self,elements:Set, topology:Set):
        self.X = elements # The underlying set should saved seperately from the topology
        self.topology = topology # The topology which the feature added by a topological space should be stored
        if not self.verifyTopology():
            raise ValueError("Topology not valid for given underlying set")
        
    def verifyTopology(self):
        # Check to make sure that the empty set is within the topology
        if [] not in self.topology:
            print ("Empty Set not in topology")
            return False
        
        # Check to see the entire underlying set is in the topology
        if [].append(self.X) not in self.topology:
            print ("Underlying set is not within the topology")
            return False

        # Check to see if the topology is closed under the union operation
        for subset_a in self.topology:
            for subset_b in self.topology:
                if list(set(subset_a).union(set(subset_b))) not in self.topology:
                    print("Topology is not closed under union")
                    return False
                
        # Check to see if the topology is closed under the intersection operation
        for subset_a in self.topology:
            for subset_b in self.topology:
                if list(set(subset_a).intersection(set(subset_b))) not in self.topology:
                    print("Topology is not closed under finite intersection")
                    return False

        return True

    def returnObject(self):
        object = []
        object.append(self.X)
        object.append(self.topology)
        return object

class continuousFunction(function):
    pass