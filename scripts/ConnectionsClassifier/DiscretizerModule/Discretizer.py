import abc

class Discretizer(metaclass=abc.ABCMeta):
    """Abstract class that contains the methods to:
        * create the intervals as a list of floats. 
        * discretize one value (get the bin where that value is included in the bounds)

    The list of floats is structured in this way:
    Given a set of intervals where:
        * let :math:`n` the number of interval
        * the list has :math:`n + 1` elements
        * let :math:`i`, :math:`0 <= i <= n:`
        * :math:`l_i` is the lower bound of the :math:`i`-nth interval
        * :math:`u_i` is the upper bound of the :math:`i`-nth interval

    the list will be like this
    [ :math:`l_1, u_1/l_2, u_2/l_3, ... , u_{n-1}/l_n, u_n`]
    where :math:`u_{i-1}/l_i` means that the element is both the upper bound of
    the :math:`(i-1)`-nth interval and the lower bound of the :math:`i`-nth element

    :param __discretized_bins: list that contains the intervals after calling discretize
    :type __discretized_bins: list
    :param __n_bins: number of bins for this discretization
    :type __n_bins: int
    """
    def __init__(self, n_bins: int=None) -> None:
        """Constructor that initialize discretized_bins with and empty list

        :param n_bins: number of bins, defaults to None
        :type n_bins: int, optional
        """
        self._discretized_bins = []
        self._n_bins = n_bins

    def get_discretized_bins(self) -> list:
        """Getter of the discretized bins list

        :return: the discretized list
        :rtype: list
        """
        return self._discretized_bins
    
    def get_n_bins(self) -> list:
        """Getter of the number of bins for this discretizer

        :return: the number of bins
        :rtype: list
        """
        return self._n_bins

    @abc.abstractmethod
    def discretize(self, values: list) -> None:
        """Analizes the list of values in input to create the bins

        :param values: list of values to discretize
        :type values: list
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
        for i in range(len(self._discretized_bins) - 1):
            lower = self._discretized_bins[i]
            upper = self._discretized_bins[i + 1]
            if lower <= value <= upper:
                return f'[{lower}, {upper}['
                
        return 'value out of bounds'