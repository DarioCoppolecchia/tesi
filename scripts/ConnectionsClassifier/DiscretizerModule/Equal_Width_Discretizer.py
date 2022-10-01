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

    def discretize(self, values: list) -> list:
        """Analizes the list of values in input to create the bins

        :param values: list of values to discretize with equal width
        :type values: list
        :return: the discretized list
        :rtype: list
        """
        from math import inf
        min_val = min(values)
        max_val = max(values)
        step = (max_val - min_val) / self.n_bins
        self.discretized_bins = [-inf] + [min_val + step * i for i in range(1, self.n_bins)] + [inf]
