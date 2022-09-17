import abc
from typing import Any # to create an abstract class

class Discretizer(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.discretized_bins = []

    @abc.abstractmethod
    def discretize(self, values: list):
        pass

    @abc.abstractmethod
    def discretize_attribute(self, value: float):
        pass

class Equal_Height_Discretizer(Discretizer):
    def discretize_attribute(self, value: float):
        pass

class Equal_Width_Discretizer(Discretizer):

    def __init__(self, min: float, max: float, n_bins: int) -> None:
        super().__init__()
        self.min = min
        self.max = max
        self.n_bins = n_bins

    def discretize_attribute(self, value: float):
        pass
    
    def set_min(self, min: float):
        self.min = min
    def set_max(self, max: float):
        self.max = max
    def set_n_bin(self, n_bin: int):
        self.n_bin = n_bin
    def get_min(self) -> float:
        return self.min
    def get_max(self) -> float:
        return self.max
    def get_n_bins(self) -> int:
        return self.n_bins