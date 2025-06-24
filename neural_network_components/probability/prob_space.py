from categories.MeasurableSpace import meas
from categories.Set import Set
from constants import random
class ProbSpace(meas):
    def __init__(self, elements:Set, sigma_algebra:list[list], measure:dict[list, float], R=False):
        super().__init__(elements, sigma_algebra)
        if not self._verifyMeasure():
            raise TypeError("Invalid Measure Given")
        self.measure=self._normalize_measure(measure)
        self.R = R
        
    def _verifyMeasure(self,measure:dict[list,float]):
        for item in measure.items():
            if item not in self.sigma_algebra:
                return False
        return True
    
    def _normalize_measure(self,measure:dict[list,float]):
        sumMeasures = sum(measure.values())
        normalizedMeasure = {list:float}
        for item in measure.items():
            newMeasure = measure.get(item)/sumMeasures
            normalizedMeasure.update(item,newMeasure)
        return normalizedMeasure
    
    def randomSample(self):
        if not self.R:
            cumulative = 0
            rand = random(1.0)
            for subset, prob in self.measure.items():
                cumulative = cumulative + prob
                if rand<cumulative:
                    return subset
            return None
        else:
            pass
    
    def pdf(self,subset):
        if not self.R:
            return self.measure.get(subset, 0.0)
        else:
            pass
    
    def cdf(self,subset):
        if not self.R:
            cumalative = 0
            for subsetOfMeasure in sorted(self.measure.keys()): 
                cumalative = cumalative + self.measure[subsetOfMeasure]
                if subsetOfMeasure == subset:
                    break
            return cumalative
    
    def expected_value(self, randomVariable:dict[list,float]):
        if not self.R:
            expected = 0
            for subset, measure in randomVariable.items():
                expected = measure * self.measure.get(subset,0.0)
            return expected
    
    def variance(self,randomVariable:dict[list,float]):
        if not self.R:
            expected = self.expected_value(randomVariable)
            expected_square = sum((value**2)*self.measure.get(subset,0.0) for subset, value in randomVariable.items())
            return expected_square-(expected**2)




    
