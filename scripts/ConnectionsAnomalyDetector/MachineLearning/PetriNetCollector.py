from pandas import DataFrame
from .PetriNet import PetriNet
import pm4py

class PetriNetCollector:
    def __init__(self, attrs: list, delta: float) -> None:
        self.__dict_petriNet = {}
        self.__delta = delta
        for attr in attrs:
            self.__dict_petriNet[attr] = PetriNet()
    
    def load_xes(self, file_name: str) -> None:
        self.__data_log = pm4py.read_xes(file_name)

    def train(self) -> None:
        for attr, pn in self.__dict_petriNet.items():
            pn.train(self.__data_log, self.__delta, f'concept:{attr}')

    def create_PetriNet_dataset(self) -> DataFrame:
        print(list(self.__dict_petriNet.values())[0].calc_conformance(self.__data_log))
        #return DataFrame([pn.calc_conformance(self.__data_log) for pn in self.__dict_petriNet.values()])