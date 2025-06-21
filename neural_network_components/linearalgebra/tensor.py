from categories.Category import Object
from categories.matrix import Matrix

class tensor(Object):
    ## Initialize the tensor; if there is a prexisting tensor  "data" all it to be stored in that directly
    ## if not, we need a shape to initalize a tensor with just zeros
    def __init__(self, data=None, shape=None):
        if data == None:
            if shape == None:
                raise ValueError("Either shape or data should be provided")
            else:
                self.X = self._initialize_zeros(shape)
                self.shape = shape
        else:
            if not self._verifyTensor(data):
                raise ValueError("Incorrect data provided")
            else:
                self.X = data
                self.shape = self._inferShape(data)

    ## Initializing the zeros by the shape, recursively call the the method to created a nested list
    ## based on the given shape given
    def _initialize_zeros(self,shape):
        if len(shape)==1:
            return[0]*shape[0] # Base Case
        for _ in range(shape[0]):
            return [self._initialize_zeros(shape[1:])] 
    
    ## If we are given the data, we should guess what the shape is. To do this, we can recursively call
    ## the method summing the number of times we are going inside the list.
    def _inferShape(self,data):
        if not isinstance(data,list):
            return []
        return [len(data)]+self._inferShape(data[0])
    
    ## To verify that it is a tensor, we similarly recursively call inside and make sure that the length of each 
    ## sublist remains constant. We recursively go through the tensor to make sure that this is the case.
    def _verifyTensor(self,data):
        if not isinstance(data,list):
            return True
        lengths = [len(sublist) for sublist in data]
        return all(1==lengths[0] for l in lengths) and all(self._verifyTensor(sublist) for sublist in data)


    ## Reshaping the tensor. To reshape the tensor, the following steps are taken. First we have to flatten the
    ## tensor and confirm that the new shape can hold the elements of the tensor. Then we unflatten the data so 
    ## that it fits under the bounds of the new shape

    def reshape(self,newshape):
        flattenedData = self._flattenData(self.X)
        if len(flattenedData) != self._total_elements(newshape):
            raise ValueError("The number of elements of the new shape does not matches with the number of items")
        self.X = self._unflattenData(flattenedData,newshape)
        self.shape = newshape

    ## Flattening the data means compressing all the elements into a 1D array to know how many elements there are
    def _flattenData(self, data):
        if not isinstance(data,list):
            return [data]
        return [x for sublist in data for x in self._flattenData(sublist)]
    
    ## Unflattening basically uses the same concept as initializing zeros but under the constraint of the new shape and the
    ## total size of the array that we are dealing with
    def _unflattenData(self,data,shape):
        if len(shape) == 1:
            return data[:shape[0]]
        size = self._total_elements(shape[1:])
        return [self._unflattenData(data[i * size:(i + 1) * size], shape[1:]) for i in range(shape[0])]
    
    # Simple method that counts the total number of elements in the tensor
    def _total_elements(self,shape):
        total = 1
        for val in shape:
            total = total * val
        return total
   
    # Inherited return object method, for all purposes returning X is fine.
    def returnObject(self):
        return super().returnObject()
        
    ## TODO: Element‑wise Opperations + Broadcasting
    def dot(self):
        pass

    ## TODO: Gradient Tracking (Requires fixing of the graph class)