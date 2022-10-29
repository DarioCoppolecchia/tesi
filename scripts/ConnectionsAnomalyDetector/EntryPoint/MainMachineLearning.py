from MachineLearning.AnomalyDetector    import AnomalyDetector
from MachineLearning.PetriNetCollector  import PetriNetCollector

class MainMachineLearning:
    def __init__(self, config_path: str='') -> None:
        self.start_application(config_path)
        self.execute_application()

    def start_application(self, config_path: str='') -> None:
        self.__anomaly_detector = AnomalyDetector()
        self.__petriNetCollector = PetriNetCollector()

    def execute_application(self) -> None:
        self.__train_model()
        self.__test_model()

    def __train_model():
        pass

    def __test_model():
        pass

main = MainMachineLearning('config.ini')