from pandas import DataFrame
from .PetriNet import PetriNet
import pm4py
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.obj import Trace
from pm4py.objects.log.obj import Event
import tqdm

class PetriNetCollector:
    def __init__(self, attrs: list, delta: float) -> None:
        self.__dict_petriNet = {}
        self.__delta = delta
        for attr in attrs:
            self.__dict_petriNet[f'concept:{attr}'] = PetriNet()
    
    def load_xes(self, file_name: str) -> None:
        self.__data_log = pm4py.read_xes(file_name)

    def train(self) -> None:
        for attr, pn in self.__dict_petriNet.items():
            pn.train(self.__data_log, self.__delta, attr)

    def create_PetriNet_dataset(self) -> DataFrame:
        df = DataFrame()
        res = [0 for _ in self.__dict_petriNet.values()]
        for i, (attr, pn) in enumerate(tqdm.tqdm(self.__dict_petriNet.items())):
            for trace in self.__data_log:
                trace_temp = Trace()
                #trace_temp.attributes = copy.deepcopy(trace.attributes)
                for event in trace:
                    event_temp = Event()
                    for key in event:
                        if key != attr:
                            event_temp[key] = event[key]
                        else:
                            event_temp['Activity'] = event[key]
                    trace_temp.append(event_temp)
                log = EventLog([trace_temp])
                res[i] = pn.calc_conformance(log)['average_trace_fitness']
            df[attr] = res
        return df