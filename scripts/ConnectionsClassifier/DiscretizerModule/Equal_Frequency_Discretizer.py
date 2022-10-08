from . import Discretizer

class Equal_Frequency_Discretizer(Discretizer):
    """
    Class that discretize with the Equal Frequency algorithm a list of values and 
    returns the bin relative to a particulare value
    """    

    def __init__(self, n_bins: int=None):
        """
        Constructor of this class, calls the super constructor

        :param n_bins: number of bins, defaults to None
        :type n_bins: int, optional
        """
        super().__init__(n_bins)

    def discretize(self, values: list) -> list:
        """Analizes the list of values in input to create the bins

        :param values: list of values to discretize with equal Frequency
        :type values: list
        :return: the discretized list
        :rtype: list
        """
        from math import inf
        values.sort()
        step = int(len(values) / self._n_bins)
        self._discretized_bins = [-inf] + [values[step * i] for i in range(1, self._n_bins)] + [inf]

        