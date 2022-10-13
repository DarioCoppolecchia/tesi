from . import Discretizer

class Equal_Width_Discretizer(Discretizer):
    """
    Class that discretize with the Equal width algorithm a list of values and 
    returns the bin relative to a particulare value
    """

    def __init__(self, n_bins: int=None, soglia: int=None) -> None:
        """Constructor of this class, calls the super constructor
        and initializes the parameters

        :param n_bins: number of bins , defaults to None
        :type n_bins: int, optional
        """
        super().__init__(n_bins, soglia)


    def discretize(self, values: list) -> None:
        """Analizes the list of values in input to create the bins

        :param values: list of values to discretize with equal width
        :type values: list
        """
        from math import inf

        val_set = set(values)
        value_set_len = len(val_set)
        if value_set_len <= max(self._n_bins, self._SOGLIA):
            values = sorted(list(val_set))
            self._discretized_bins = [-inf] + [(values[i] + values[i - 1]) / 2 for i in range(1, value_set_len)] + [inf]
        else:
            min_val = min(values)
            max_val = max(values)
            step = (max_val - min_val) / self._n_bins
            self._discretized_bins = [-inf] + [min_val + step * i for i in range(1, self._n_bins)] + [inf]

