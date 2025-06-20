from categories.MeasurableSpace import meas
from categories.Set import Set
class ProbSpace(meas):
    def __init__(self, elements:Set, sigma_algebra:list[list], measure:dict[tuple, float]):
        super().__init__(elements, sigma_algebra, measure)
        self._normalize_measure()
        if not self._is_probability_measure():
            raise ValueError("Total measure must be 1")
