from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from pandas import DataFrame
import pickle

class AnomalyDetector:
    def __init__(self) -> None:
        self.__model = IsolationForest()

    def train(self, dataset: DataFrame):
        # TODO
        self.__model.fit(dataset)

    def test(self, dataset: DataFrame) -> DataFrame:
        # TODO
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
