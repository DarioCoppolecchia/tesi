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
        value_set_len = len(set(values)) - 1
        if value_set_len < self._n_bins:
            self._n_bins = value_set_len
        step = int(len(values) / self._n_bins)
        self._discretized_bins = [-inf] + [values[step * i] for i in range(1, self._n_bins)] + [inf]

        # from math import inf
        # values_set = set(values)
        # value_set_len = len(values_set) - 1
        # values = sorted(list(values_set))
        # if value_set_len < self._n_bins:
        #     print(set(values))
        #     self._n_bins = value_set_len
        # step = int(len(values) / self._n_bins)
        # self._discretized_bins = [-inf] + [values[step * i] for i in range(1, self._n_bins)] + [inf]






# from random import randint

# dict_perc = {
#     '0.0-0.5': 0,
#     '0.5-0.55': 1,
#     '0.55-0.6': 2,
#     '0.6-0.8': 3,
#     '0.8-0.9': 4,
#     '0.9-0.92': 5,
#     '0.92-0.94': 6,
#     '0.94-0.96': 7,
#     '0.96-0.98': 8,
#     '0.98-1': 9,
# }

# def random_with_perc(dict_perc: dict, n: int) -> list:
#     from random import uniform
#     arr = [0 for _ in range(n)]
#     for i, _ in enumerate(arr):
#         val = uniform(0, 1)
#         for interval, value in dict_perc.items():
#             int_parsed = [float(bound) for bound in interval.split('-')]
#             arr[i] += value if int_parsed[0] <= val < int_parsed[1] else 0
#     return arr
    
# def count_if(arr, val):
#     return sum([1 for e in arr if e == val])

# _n_bins = 10
# values = random_with_perc(dict_perc, 1000)
# for val in dict_perc.values():
#     print(f"{val}: {count_if(values, val)}")
# #values.sort()

# from math import inf
# values_set = set(values)
# value_set_len = len(values_set) - 1
# values = sorted(list(values_set))
# if value_set_len < _n_bins:
#     print(set(values))
#     _n_bins = value_set_len
# step = int(len(values) / _n_bins)
# _discretized_bins = [-inf] + [values[step * i] for i in range(1, _n_bins)] + [inf]
# print(_discretized_bins)


        