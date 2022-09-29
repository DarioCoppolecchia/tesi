import Discretizer

class Equal_Height_Discretizer(Discretizer):
    """
    Class that discretize with the Equal height algorithm a list of values and 
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

        :param values: list of values to discretize with equal height
        :type values: list
        :return: the discretized list
        :rtype: list
        """
        pass

    def discretize_attribute(self, value: float) -> str:
        """Given a value such that: min(discretized_bins) <= value <= max(discretized_bins), 
        this returns the bin associated to that value using the equal height algorithm

        :param value: value to discretize
        :type value: float
        :return: the return dipends on the value in input is a string representing the bounds of the interval

        :rtype: str
        """
        pass