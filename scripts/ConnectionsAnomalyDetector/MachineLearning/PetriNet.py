from pandas import DataFrame
import pm4py
from pm4py.algo.discovery.inductive import algorithm as ind_miner
from pm4py.algo.discovery.inductive.variants.im_f.algorithm import Parameters
from pm4py.objects.conversion.process_tree import converter

class PetriNet:
    def train(self, xes_log: pm4py.objects.log.obj.EventLog, delta: float, activity: str) -> None:
        ptree = ind_miner.apply_tree(xes_log, parameters={Parameters.NOISE_THRESHOLD: delta, Parameters.ACTIVITY_KEY: activity}, variant=ind_miner.Variants.IMf)
        self.__model = converter.apply(ptree)

    def calc_conformance(self, xes_log: pm4py.objects.log.obj.EventLog) -> DataFrame:
        if type(self.__model) == tuple: # check if the model has been created
            return pm4py.fitness_alignments(xes_log, self.__model[0], self.__model[1], self.__model[2], multi_processing=True)
        raise TypeError('The petri net has not been discovered yet, or is not a tuple')

    def save_model(self, file_name: str) -> None:
        pm4py.write_pnml(self.__model[0], self.__model[1], self.__model[2], file_name)

    @classmethod
    def load_model(file_name: str):
        temp = PetriNet()
        temp.__model = pm4py.read_pnml(file_name)
        return temp