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
            "verbose": 0,
            "warm_start": False,
        }

        self.__model = IsolationForest(**hyperparameters)

    def train(self, dataset: DataFrame, file_name: str) -> None:
        import os
        from os.path import exists

        print(dataset)

        try:
            os.makedirs(file_name[:file_name.rfind('/')+1]) # create the folder if isn't already present
        except:
            pass

        if not exists(file_name): # train the model only if isn't already present in the folder
            print('Creating the model...')
            for attr in dataset:
                self.__model.fit(np.array(dataset[attr]).reshape(-1, 1))
            self.save_model(file_name)
        else:
            print('Loading the model...')
            self.__model = AnomalyDetector.load_model(file_name).__model

    def predict(self, dataset: DataFrame) -> DataFrame:
        preds = DataFrame()
        print(dataset)
        for attr in dataset:
            temp = np.array(dataset[attr])
            preds[attr] = self.__model.predict(temp.reshape(-1, 1))
        return preds

    def create_confusion_matrix(self, Y: np.ndarray, y_pred: DataFrame) -> str:
        print(Y)
        print(y_pred)
        tot_len = Y.shape[0]
        for attr in Y:
            tot_pred_corr = sum([y == y_0 for y, y_0 in zip(Y[attr], y_pred[attr])])
            print(f'Classification report per attr: {attr}, accuracy: {tot_pred_corr}/{tot_len} ({tot_pred_corr / tot_len * 100})')
            #print(classification_report(Y[attr], y_pred[attr]))

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
