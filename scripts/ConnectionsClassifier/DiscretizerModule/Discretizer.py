import abc
from typing import Any # to create an abstract class

class Discretizer(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.attribute = 0

    @abc.abstractmethod
    def discretize_attribute(self, values: list):
        pass

    @abc.abstractmethod
    def get_attribute(self) -> Any:
        return self.attribute

class Equal_Height_Discretizer(Discretizer):
    def discretize_attribute(self, values: list):
        pass

    def get_attribute(self) -> Any:
        return self.attribute

class Equal_Width_Discretizer(Discretizer):
    def discretize_attribute(self, values: list):
        pass

    def get_attribute(self) -> Any:
        return self.attribute