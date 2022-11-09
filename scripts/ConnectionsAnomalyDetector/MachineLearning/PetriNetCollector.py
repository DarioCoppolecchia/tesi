from pandas import DataFrame
from .PetriNet import PetriNet
import pm4py
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.obj import Trace
from pm4py.objects.log.obj import Event
import tqdm
import numpy as np

class PetriNetCollector:
    def __init__(self, attrs: list, delta: float) -> None:
        self.__dict_petriNet = {}
        self.__delta = delta
        for attr in attrs:
            self.__dict_petriNet[f'concept:{attr}'] = PetriNet()
    
    def load_xes(self, file_name: str) -> None:
        self.__data_log = pm4py.read_xes(file_name)

    def train(self, file_name: str) -> bool:
        import os
        from os.path import exists
        saved = True
        for attr, pn in tqdm.tqdm(self.__dict_petriNet.items()):
            file_name_complete = f'{file_name}_{attr}.pnml'
            if not exists(file_name_complete): # train the model only if isn't already present in the folder
                saved &= False
                pn.train(self.__data_log, self.__delta, attr)
                try:
                    os.mkdir(file_name[:file_name.rfind('/')+1]) # create the folder if isn't already present
                except:
                    pass
            else:
                self.load_model(file_name_complete)
        return saved

    def create_PetriNet_dataset(self) -> DataFrame:
        df = DataFrame()
        Y = DataFrame()
        res = [0 for _ in self.__data_log]
        y_res = [0 for _ in self.__data_log]
        for attr, pn in self.__dict_petriNet.items():
            print(f'Creating PetriNet Dataset for the attribute {attr}')
            for i, trace in enumerate(tqdm.tqdm(self.__data_log)):
                trace_temp = Trace()
                y_res[i] = 1 if trace.attributes['concept:label'] == 'Normal' else -1
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
            Y[attr] = y_res
            print('')
        return df, Y

    def save_model(self, file_name: str) -> None:
        for attr, pn in self.__dict_petriNet.items():
            print(f'il cazzo di attr: {attr.replace("concept:", "")}')
            pn.save_model(f'{file_name}_{attr.replace("concept:", "")}.pnml')

    def load_model(self, file_name: str):
        for attr in self.__dict_petriNet:
            print(f'u stoc a carca: {attr.replace("concept:", "")}')
            self.__dict_petriNet[attr] = PetriNet.load_model(f'{file_name}_{attr.replace("concept:", "")}.pnml')