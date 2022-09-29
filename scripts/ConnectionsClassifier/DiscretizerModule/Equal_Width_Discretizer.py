import Discretizer

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
        pass

    def discretize_attribute(self, value: float) -> tuple:
        """Given a value such that: min(discretized_bins) <= value <= max(discretized_bins), 
        this returns the bin associated to that value using the equal height algorithm

        :param value: value to discretize
        :type value: float
        :return: the return dipends on the value in input: if the value is between lower bound and upper bound, this returns the bounds as a tuple (lower bound, upper bound), else return a tuple with (0, 0)

        :rtype: tuple
        """
        pass