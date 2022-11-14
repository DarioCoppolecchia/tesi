from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
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

        print('Dataset Training:\n', dataset)

        try:
            os.makedirs(file_name[:file_name.rfind('/')+1]) # create the folder if isn't already present
        except:
            pass

        if not exists(file_name): # train the model only if isn't already present in the folder
            print('Creating the model...')
            self.__model.fit(dataset)
            self.save_model(file_name)
        else:
            print('Loading the model...')
            self.__model = AnomalyDetector.load_model(file_name).__model

    def predict(self, dataset: DataFrame) -> DataFrame:
        print('Dataset predizione:\n', dataset)
        return self.__model.predict(dataset)

    def create_confusion_matrix(self, Y: np.ndarray, y_pred: DataFrame) -> str:
        Y = np.array(Y)
        y_pred = np.array(y_pred)
        tot_len = len(Y)
        tot_pred_corr = sum([y == y_0 for y, y_0 in zip(Y, y_pred)])
        print(f'Classification report accuracy: {tot_pred_corr}/{tot_len} ({tot_pred_corr / tot_len * 100})')
        print(classification_report(Y, y_pred))

        cm = confusion_matrix(Y, y_pred)
        cm_display = ConfusionMatrixDisplay(confusion_matrix = cm)
        cm_display.plot()
        plt.show()

        val_to_labels = {-1: 'Anomaly', 1: 'Normal'}
        Y = np.vectorize(val_to_labels.get)(Y)
        y_pred = np.vectorize(val_to_labels.get)(y_pred)
        cm = confusion_matrix(Y, y_pred, labels=['Anomaly', 'Normal'])
        cm_display = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels=['Anomaly', 'Normal'])
        cm_display.plot()
        plt.show()

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
