from pandas import DataFrame
import pm4py

class PetriNet:
    def train(self, xes_log: pm4py.objects.log.obj.EventLog, delta: float, activity: str) -> None:
        # TODO: gestire il delta e la scelta dell'activity (forse da spostare solo in PetriNetCollector)
        self.__model = pm4py.discover_petri_net_alpha(xes_log)

    def calc_conformance(self, xes_log: pm4py.objects.log.obj.EventLog) -> DataFrame:
        if type(self.__model) == tuple: # check if the model has been created
            # return pm4py.conformance_diagnostics_alignments(xes_log, self.__model[0], self.__model[1], self.__model[2], multi_processing=True)
            # return pm4py.conformance_alignments(xes_log, self.__model[0], self.__model[1], self.__model[2])
            return pm4py.conformance_diagnostics_token_based_replay(xes_log, self.__model[0], self.__model[1], self.__model[2])
        raise TypeError('The petri net has not been discovered yet, or is not a tuple')

    def save_model(self, file_name: str) -> None:
        pm4py.write_pnml(self.__model[0], self.__model[1], self.__model[2], file_name)

    @classmethod
    def load_model(file_name: str):
        temp = PetriNet()
        temp.__model = pm4py.read_pnml(file_name)
        return temp