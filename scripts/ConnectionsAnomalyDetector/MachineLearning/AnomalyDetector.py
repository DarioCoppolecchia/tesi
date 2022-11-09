from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from pandas import DataFrame
import pickle
import numpy as np

class AnomalyDetector:
    def __init__(self) -> None:
        hyperparameters = {
            "n_estimators": 100,
            "max_samples": 'auto', # può anche essere un intero o un float
            "contamination": 'auto', # può anche essere un float
            "max_features": 1.0, 
            "bootstrap": False,
            "n_jobs": -1, # multiprocessing
            "random_state": 42,
            "verbose": 2,
            "warm_start": False,
        }

        self.__model = IsolationForest(**hyperparameters)

    def train(self, dataset: DataFrame, file_name: str) -> None:
        import os
        from os.path import exists
        if not exists(file_name): # train the model only if isn't already present in the folder
            for attr in dataset:
                self.__model.fit(np.array(dataset[attr]).reshape(-1, 1))
            try:
                os.mkdir(file_name[:file_name.rfind('/')+1]) # create the folder if isn't already present
            except:
                pass
            self.save_model(file_name)
        else:
            self.__model = AnomalyDetector.load_model(file_name).__model

    def predict(self, dataset: DataFrame) -> DataFrame:
        preds = DataFrame()
        for attr in dataset:
            temp = np.array(dataset[attr])
            preds[attr] = self.__model.predict(temp.reshape(-1, 1))
        return preds

    def create_confusion_matrix(self, Y: np.ndarray, y_pred: DataFrame) -> str:
        print(classification_report(Y, y_pred))

    def save_model(self, file_name: str):
        with open(file_name,'wb') as f:
            pickle.dump(self.__model,f)

    @classmethod
    def load_model(cls, file_name: str):
        with open(file_name,'rb') as f:
            temp = AnomalyDetector()
            temp.__model = pickle.load(f)
            return temp
        raise FileNotFoundError(f'File of model not found at location: "{file_name}"')
