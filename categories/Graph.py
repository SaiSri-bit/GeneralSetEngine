from Set import Set, function
from Category import Object,Morphism

class grph(Object):
    def __init__(self,vertexs:Set, edges:list):
        # Store all the vertex in a list. This will help keep track of them if they are needed later
        # Do the same with the edges.
        self.vertexs = vertexs.getSet
        self.edges = edges

        # The purpose of the label keys is to act as a map between the actual index and their placement
        # in the adjaceny matrix. This allows for seamless transitions when doing calculations with the
        # graph and the element in the set may not be actually representative of its index in the matrix
        self.labelkeys:dict = {} 
        for index in range(len(self.vertexs)):
            self.labelkeys.update({self.vertexs[index]:index})

        # Storing the adjacency matrix as a vertex x vertex array. To do so will have to first make a new
        # row list of the size of len(vertex) for each vertex and add it into the matrix
        matrix = []
        for value in self.vertexs:
            row = []
            for value2 in self.vertexs:
                row.append(0)
            matrix.append(row)
        
        # When we are adding in edges we have to be sure of a few things. Firstly this assumes that edges
        # will be of the form (Start Stop Weight) as a tuple. Weight must be an index. Within the set class
        # characters are alled to be in the set. This means that the start and stop can be properly mapped in
        # the index. On the other hand, weigth has to be viewed as a int or float to not cause problems later
        for value in edges:
            if type(value)!=tuple:
                raise TypeError("List of edges contains nontuples")
            if len(value) != 3:
                raise TypeError("Format should be Vertex_1 Vertex_2 Edge_Weigth")
            if type(value[3]) != int or type(value[3]) !=float:
                raise TypeError ("Edge Weight must be int or float")
            index1 = self.labelkeys.get(value[0])
            index2 = self.labelkeys.get(value[1])
            matrix[index1][index2] = value[2]

        # After this is the done, the main "object" of the grph class will be treated as this adjacency matrix
        # which is why it will be stored as X.
        self.X = matrix

    def returnEdgeWeight(self,element:tuple):
        # To find edge weights we have to know the start and stop. In directed graphs order matters, and 
        # in nondirected graphs, order does not. The grph class will always assume that it is a directed
        # graph and if it is undirected, then it will be treated where the same weight is same going 
        # from each direction
        if len(element)!=2:
            raise ValueError("Tuple size should be 2, start vertex end vertex")
        if element[2]==0:
            print ("Edge Value is being set to 0... Edge is being deleted")
        index1 = self.labelkeys.get(element[0])
        index2 = self.labelkeys.get(element[1])
        return self.X[index1][index2]
    
    def add_vertex(self, element):
        # When adding a new vertex, we should always first add into the map. This way we can keep track
        # of the specific spot of the new element and be able to recall it using said element. Along with
        # that, add the new vertex into the list of all vertexs to keep track of the new vertex
        self.labelkeys.update({element:len(self.X)})
        self.vertexs.append(element)

        # Then we have to first create a new column in the matrix. To do so, a weight of 0 is added to
        # the end of each row as you go down
        for row in self.X:
            row.append(0)

        # From there a new final row will be added at the bottom connected with the new row length
        new_row = []
        for val in self.X[0]:
            new_row.append(0)
        self.X.append(new_row)
        

    def add_edge (self,edge:tuple):
        if len(edge)!=3:
            raise ValueError("Edge Tuple can only contain 3 elements, start stop weight")
        if type(edge[2]) != int or type(edge[2]) != float:
            raise TypeError("The type of the edge weight must be an int or float")
        index1=self.labelkeys.get(edge[0])
        index2=self.labelkeys.get(edge[1])
        self.X[index1][index2]=edge[2]
        self.edges.append(edge)

    def dijkstra(self,source,stop):
        pass

    def bfs(self,source,stop):
        queue = []
        startIndex = self.labelkeys.get(source)
        stopIndex = self.labelkeys.get(stop)


    def cycleChecker(self):
        pass

    def minSpanTreePrims(self):
        pass

    def maxFlow(self):
        pass



class grphHomomorphism(Morphism):
    pass