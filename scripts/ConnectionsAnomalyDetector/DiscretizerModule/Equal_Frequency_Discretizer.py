from . import Discretizer

class Equal_Frequency_Discretizer(Discretizer):
    """
    Class that discretize with the Equal Frequency algorithm a list of values and 
    returns the bin relative to a particulare value
    """    

    def __init__(self, n_bins: int=None, soglia: int=None, filepath: str='', save: bool=False):
        """
        Constructor of this class, calls the super constructor

        :param n_bins: number of bins, defaults to None
        :type n_bins: int, optional
        """
        super().__init__(n_bins, soglia, filepath, save)

    def discretize(self, values: list) -> None:
        """Analizes the list of values in input to create the bins

        :param values: list of values to discretize with equal Frequency
        :type values: list
        :return: the discretized list
        :rtype: list
        """
        import pickle

        if self._save:
            from math import inf
            val_set = set(values)
            value_set_len = len(val_set)

            # handling distinct values
            if value_set_len <= max(self._n_bins, self._SOGLIA):
                values = sorted(list(val_set))
                self._discretized_bins = [-inf] + [(values[i] + values[i - 1]) / 2 for i in range(1, value_set_len)] + [inf]# + ['soglia']
            else:
                values.sort()
                step = int(len(values) / self._n_bins)
                self._discretized_bins = [-inf] + [values[step * i] for i in range(1, self._n_bins)] + [inf]
                
                disc_set = list(set(self._discretized_bins))
                if len(disc_set) < len(self._discretized_bins):
                    self._discretized_bins = sorted(disc_set)# + ['con duplicati']
                
            with open(self._filepath, 'wb') as f:
                obj = {
                    '_n_bins': self._n_bins,
                    '_SOGLIA': self._SOGLIA,
                    '_discretized_bins': self._discretized_bins,
                }
                
                pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        else:
            with open(self._filepath, 'rb') as f:
                obj = pickle.load(f)

            self._n_bins = obj['_n_bins']
            self._SOGLIA = obj['_SOGLIA']
            self._discretized_bins = obj['_discretized_bins']
            
            import numpy as np
            print(self._filepath.split('/')[-1])
            print(self._n_bins)
            print(self._SOGLIA)
            print(np.array(self._discretized_bins))
            print('\n')