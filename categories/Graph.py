from .Set import Set, function
from .Category import Object,Morphism
from .matrix import Matrix
class grph(Object):
    def __init__(self,vertexs:Set, edges:Set):
        ## Verify that the edges given are valid in relation to the vertex
        if not self.verifyGraph(vertexs.getSet(),edges.getSet()):
            raise TypeError("Values provided do not form graph")
        self.vertexs = vertexs
        self.edges = edges

        ## Initialize a matrix which will hold the weights
        size = len(vertexs)
        setupMatrix = Matrix(size,size)
        self.X = setupMatrix.X

        ## Go through each edge and store the third value as the weight of the edge
        for edge in edges.getSet():
            self.X[edge[0]][edge[1]] = edge[2]
    
    def update_weight(self, edge:tuple):
        ## First check and see if the edge is present
        if not edge[0] in self.vertexs or not edge[1] in self.vertexs:
            raise ValueError("Vertex is missing")
        
        ## Swap whatever is the existing value with the new edges
        self.X[edge[0][edge[1]]]=edge[2]


    def verifyGraph(self,vertexs,edges):
        ## Check and confirm that all edges are valid and have a matching vertex
        for edge in edges:
            if not edge[0] in vertexs or not edge[1] in vertexs:
                return False
        return True            


        
    # def bfs(self,source,stop):
    #     queue = []
    #     startIndex = self.labelkeys.get(source)
    #     stopIndex = self.labelkeys.get(stop)
    #     seen = []
    #     distance = []
    #     for val in range(len(self.vertexs)):
    #         seen.append(-1)
    #         distance.append(0)
    #     queue.append(startIndex)
    #     distanceFromStart = 0
    #     while len(queue)!=0:
    #         index = queue.pop(0)
    #         location = 0
    #         for val in self.X[index]:
    #             if val !=0:
    #                 if seen == -1:
    #                     if location == stopIndex: 
    #                         return distanceFromStart
    #                     queue.append(location)
    #                     seen[location] = 1
    #                     distance[location] = distanceFromStart
    #             location = location+1
    #         distanceFromStart = distanceFromStart + 1


