from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from pandas import DataFrame
import pickle

class AnomalyDetector:
    def __init__(self) -> None:
        hyperparameters = {
            "n_estimetors": 100,
            "max_samples": 'auto', # può anche essere un intero o un float
            "contamination": 'auto', # può anche essere un float
            "max_features": 1.0, 
            "bootstrap": False,
            "n_jobs": -1, # multiprocessing
            "random_state": 42,
            "verbose": 10,
            "warm_start": False,
        }

        self.__model = IsolationForest(**hyperparameters)

    def train(self, dataset: DataFrame):
        self.__model.fit(dataset)

    def test(self, dataset: DataFrame) -> DataFrame:
        return self.__model.predict(dataset)

    def create_confusion_matrix(self, Y: DataFrame, y_pred: DataFrame ) -> str:
        # TODO
        classification_report(Y, y_pred)

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
