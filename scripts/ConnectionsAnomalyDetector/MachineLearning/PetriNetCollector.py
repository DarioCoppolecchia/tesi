from pandas import DataFrame
from .PetriNet import PetriNet
import pm4py
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.obj import Trace
from pm4py.objects.log.obj import Event
from tqdm.auto import tqdm
import pandas as pd
import os
from os.path import exists

class PetriNetCollector:
    def __init__(self, attrs: list, delta: float) -> None:
        self.__dict_petriNet = {}
        self.__delta = delta
        for attr in attrs:
            self.__dict_petriNet[f'concept:{attr}'] = PetriNet()
    
    def load_xes(self, file_name: str) -> None:
        self.__data_log = pm4py.read_xes(file_name)

    def train(self, file_name: str):
        saved = [] # list of the saved model attributes
        not_saved = [] # list of the not saved model attributes

        import sys

        try:
            os.makedirs(file_name[:file_name.rfind('/')+1]) # create the folder if isn't already present
        except:
            pass

        for attr, pn in tqdm(self.__dict_petriNet.items()):
            file_name_complete = f'{file_name}_{attr.replace("concept:", "")}.pnml'
            if not exists(file_name_complete): # train the model only if isn't already present in the folder
                saved.append(attr)
                pn.train(self.__data_log, self.__delta, attr)                
            else:
                not_saved.append(attr)

        self.load_model(file_name, not_saved) # load stored models
        self.save_model(file_name, saved) # saving not stored models

    def __create_dataset(self, file_name: str, attr: str, pn: PetriNet) -> tuple[list[float], list[int]]:
        res = [0 for _ in self.__data_log]
        y_res = [0 for _ in self.__data_log]

        file_name_complete = f'{file_name}_{attr.replace("concept:", "")}.csv'

        if not exists(file_name_complete):
            for i, trace in enumerate(tqdm(self.__data_log, desc=f'{attr} :: ')):
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

            DataFrame({'conformance': res, 'label': y_res}).to_csv(file_name_complete)
        else:
            df_from_file = pd.read_csv(file_name_complete)
            res = df_from_file['conformance']
            y_res = df_from_file['label']

        return res, y_res

    def create_PetriNet_dataset(self, file_name: str) -> tuple[DataFrame, DataFrame]:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        df = DataFrame()
        Y = DataFrame()

        try:
            os.makedirs(file_name[:file_name.rfind('/')+1]) # create the folder if isn't already present
        except:
            pass

        tot = len(self.__dict_petriNet)
        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = []
            for j, (attr, pn) in enumerate(self.__dict_petriNet.items()):
                futures.append(ex.submit(self.__create_dataset, file_name, attr, pn))

            for future in as_completed(futures):
                res, y_res = future.result()
                df[attr] = res
                Y[attr] = y_res
        return df, Y

    def save_model(self, file_name: str, attrs_to_save: list) -> None:
        for attr in attrs_to_save:
            self.__dict_petriNet[attr].save_model(f'{file_name}_{attr.replace("concept:", "")}.pnml')

    def load_model(self, file_name: str, attrs_to_load: list):
        for attr in attrs_to_load:
            self.__dict_petriNet[attr] = PetriNet.load_model(f'{file_name}_{attr.replace("concept:", "")}.pnml')