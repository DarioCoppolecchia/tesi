from .PetriNet import PetriNet

import pandas as pd
from pandas import DataFrame

import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event
from tqdm.auto import tqdm

import os
from os.path import exists

from multiprocessing import current_process, Pool

from pm4py.algo.discovery.inductive.variants.im_f.algorithm import Parameters

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

        try:
            os.makedirs(file_name[:file_name.rfind('/')+1]) # create the folder if isn't already present
        except:
            pass

        log = EventLog([Trace() for _ in self.__data_log])
        for attr, pn in tqdm(self.__dict_petriNet.items()):
            file_name_complete = f'{file_name}_{attr.replace("concept:", "")}.pnml'
            for i, trace in enumerate(self.__data_log):
                log[i] = Trace({'concept:name': activity[attr]} for activity in trace)
            if not exists(file_name_complete): # train the model only if isn't already present in the folder
                saved.append(attr)
                pn.train(log, self.__delta, 'concept:name')
            else:
                not_saved.append(attr)

        self.load_model(file_name, not_saved) # load stored models
        self.save_model(file_name, saved) # saving not stored models

    def create_dataset(self, args: tuple[str, str, PetriNet, int]) -> tuple[list[float], list[int]]:
        file_name, attr, pn, pos = args
        res = [0 for _ in self.__data_log]

        file_name_complete = f'{file_name}_{attr.replace("concept:", "")}.csv'

        if not exists(file_name_complete):
            with tqdm(total=len(self.__data_log), desc=f'{attr} :: ', position=pos) as pbar:
                for i, trace in enumerate(self.__data_log):
                    log= EventLog([Trace({'concept:name': activity[attr]} for activity in trace)])
                    res[i] = pn.calc_conformance(log, attr)['average_trace_fitness']
                    pbar.update(1)

            DataFrame({'conformance': res}).to_csv(file_name_complete)
        else:
            df_from_file = pd.read_csv(file_name_complete)
            res = df_from_file['conformance']

        return res

    def create_PetriNet_dataset(self, file_name: str) -> tuple[DataFrame, DataFrame]:
        df = DataFrame()
        Y = DataFrame()

        try:
            os.makedirs(file_name[:file_name.rfind('/')+1]) # create the folder if isn't already present
        except:
            pass
        
        args = [(file_name, attr, pn, i) for i, (attr, pn) in enumerate(self.__dict_petriNet.items())]

        pool = Pool()
        results = pool.map(self.create_dataset, args)

        for i, res in enumerate(results):
            attr = args[i][1]
            df[attr] = res

        return df, [1 if trace.attributes['concept:label'] == 'Normal' else -1 for trace in self.__data_log]

    def save_model(self, file_name: str, attrs_to_save: list) -> None:
        for attr in attrs_to_save:
            self.__dict_petriNet[attr].save_model(f'{file_name}_{attr.replace("concept:", "")}.pnml')

    def load_model(self, file_name: str, attrs_to_load: list):
        for attr in attrs_to_load:
            self.__dict_petriNet[attr] = PetriNet.load_model(f'{file_name}_{attr.replace("concept:", "")}.pnml')