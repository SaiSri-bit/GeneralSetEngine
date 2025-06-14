from Set import Set, function
from Category import Object,Morphism

class grph(Object):
    def __init__(self,vectors:Set, edges:list):
        self.X = vectors.getSet
        matrix = []
        for value in self.X:
            row = []
            for value2 in self.X:
                row.append(0)
            matrix.append(row)
        for value in edges:
            if type(value)!=tuple:
                raise TypeError("List of edges contains nontuples")
            if len(value) != 3:
                raise TypeError("Format should be Vertex_1 Vertex_2 Edge_Weigth")
            matrix[value[1]][value[2]] = value[3]


        
    def dijkstra(self,element):
        pass
    def bfs(self,element):
        pass
    def cycleChecker(self):
        pass
    def minSpanTreePrims(self):
        pass
    def maxFlow(self):
        pass



class grphHomomorphism(Morphism):
    pass