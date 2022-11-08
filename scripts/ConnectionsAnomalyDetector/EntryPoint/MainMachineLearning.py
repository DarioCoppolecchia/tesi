from MachineLearning.AnomalyDetector    import AnomalyDetector
from MachineLearning.PetriNetCollector  import PetriNetCollector

class MainMachineLearning:
    def __init__(self, config_path: str='') -> None:
        self.start_application(config_path)
        self.execute_application(config_path)

    def start_application(self, config_path: str='') -> None:
        import configparser

        config = configparser.ConfigParser()
        config.read(config_path)

        if 'ML' in config:
            delta = float(config['ML']['delta']) if 'delta' in config['ML'] else 0.0
        else:
            delta = 0.0

        if 'Attributes' in config:
            attrs = config['Attributes']['attributes_to_xes_events'] if 'attributes_to_xes_events' in config['Attributes'] else ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','orig_syn','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes','orig_syn','orig_fin','orig_syn_ack','orig_rst','resp_syn','resp_fin','resp_syn_ack','resp_rst','orig_bad_checksum','orig_content_gap','orig_retransmitted_payload','orig_zero_window','resp_bad_checksum','resp_content_gap','resp_retransmitted_payload','resp_zero_window','orig_ack','orig_payload','orig_inconsistent','orig_multi_flag','resp_ack','resp_payload','resp_inconsistent','resp_multi_flag']
        else:
            attrs = ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','orig_syn','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes','orig_syn','orig_fin','orig_syn_ack','orig_rst','resp_syn','resp_fin','resp_syn_ack','resp_rst','orig_bad_checksum','orig_content_gap','orig_retransmitted_payload','orig_zero_window','resp_bad_checksum','resp_content_gap','resp_retransmitted_payload','resp_zero_window','orig_ack','orig_payload','orig_inconsistent','orig_multi_flag','resp_ack','resp_payload','resp_inconsistent','resp_multi_flag']

        self.__petriNetCollector = PetriNetCollector(attrs.split(','), delta)
        self.__anomalyDetector = AnomalyDetector()

    def execute_application(self, config_path: str='') -> None:
        self.__train_model(config_path)
        self.__test_model(config_path)

    def __train_model(self, config_path: str=''):
        import configparser

        config = configparser.ConfigParser()
        config.read(config_path)

        if 'Files' in config:
            path_of_file_xes_train = config['Files']['path_of_file_xes_train'] if 'path_of_file_xes_train' in config['Files'] else '../logs/ML/conn_train.xes'
        else:
            path_of_file_xes_train = '../logs/ML/conn_train.xes'
        
        print('loading the xes train file...')
        self.__petriNetCollector.load_xes(path_of_file_xes_train)
        print('training the petriNet...')
        self.__petriNetCollector.train()
        print('creating the dataset for the Anomaly Detector...')
        dataset = self.__petriNetCollector.create_PetriNet_dataset()
        print('training the Anomaly Detector...')
        self.__anomalyDetector.train(dataset)

    def __test_model(self, config_path: str=''):
        import configparser

        config = configparser.ConfigParser()
        config.read(config_path)

        if 'Files' in config:
            path_of_file_xes_test = config['Files']['path_of_file_xes_test'] if 'path_of_file_xes_test' in config['Files'] else '../logs/ML/conn_test.xes'
        else:
            path_of_file_xes_test = '../logs/ML/conn_test.xes'
        
        print('loading the xes test file...')
        self.__petriNetCollector.load_xes(path_of_file_xes_test)
        print('creating the dataset for the Anomaly Detector...')
        dataset = self.__petriNetCollector.create_PetriNet_dataset()
        print('predicting with Anomaly Detector...')
        print(self.__anomalyDetector.predict(dataset))