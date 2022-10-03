from . import Discretizer

class Equal_Width_Discretizer(Discretizer):
    """
    Class that discretize with the Equal width algorithm a list of values and 
    returns the bin relative to a particulare value
    """

    def __init__(self, n_bins: int=None) -> None:
        """Constructor of this class, calls the super constructor
        and initializes the parameters

        :param n_bins: number of bins , defaults to None
        :type n_bins: int, optional
        """
        super().__init__(n_bins)


    def discretize(self, values: list) -> None:
        """Analizes the list of values in input to create the bins

        :param values: list of values to discretize with equal width
        :type values: list
        """
        from math import inf
        new_values = []
        for in_list in values:
            new_values += in_list
            
        for i, val in enumerate(new_values):
            if val == '-':
               new_values[i] = 0.0
        new_values = [float(val) for val in new_values]
        min_val = min(new_values)
        max_val = max(new_values)
        step = (max_val - min_val) / self._n_bins
        self._discretized_bins = [-inf] + [min_val + step * i for i in range(1, self._n_bins)] + [inf]

