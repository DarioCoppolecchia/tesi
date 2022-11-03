from MachineLearning.AnomalyDetector    import AnomalyDetector
from MachineLearning.PetriNetCollector  import PetriNetCollector

class MainMachineLearning:
    def __init__(self, config_path: str='') -> None:
        self.start_application(config_path)
        self.execute_application()

    def start_application(self, config_path: str='') -> None:
        # TODO: completare la lettura del file config.ini
        import configparser
        self.__anomaly_detector = AnomalyDetector()
        self.__petriNetCollector = PetriNetCollector()

        config = configparser.ConfigParser()
        config.read(config_path)

        # checks if Discretization is in config.ini file
        # if 'Discretization' in config:
        #     type = config['Discretization']['discretization_type'] if 'discretization_type' in config['Discretization'] else 'equal_frequency'
        #     self.__discretization_type = DISCRETIZATION_TYPE.EQUAL_FREQUENCY if type == 'equal_frequency' else DISCRETIZATION_TYPE.EQUAL_WIDTH
        #     n_bins = int(config['Discretization']['n_bins']) if 'n_bins' in config['Discretization'] else n_bins
        #     soglia = int(config['Discretization']['soglia']) if 'soglia' in config['Discretization'] else soglia
        # else:
        #     self.__discretization_type = DISCRETIZATION_TYPE.EQUAL_FREQUENCY
        #     n_bins = 5
        #     soglia = 10

        # if 'Attributes' in config:
        #     self.__activity_attr = config['Attributes']['activity_attr'] if 'activity_attr' in config['Attributes'] else 'history'
        #     self.__attr_to_xes_traces = config['Attributes']['attributes_to_xes_traces'].split(',') if 'attributes_to_xes_traces' in config['Attributes'] else ['orig_ip','orig_port','resp_ip','resp_port','proto','label']
        #     self.__attr_to_xes_events = config['Attributes']['attributes_to_xes_events'].split(',') if 'attributes_to_xes_events' in config['Attributes'] else ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes','orig_syn','orig_fin','orig_syn_ack','orig_rst','resp_syn','resp_fin','resp_syn_ack','resp_rst','orig_bad_checksum','orig_content_gap','orig_retransmitted_payload','orig_zero_window','resp_bad_checksum','resp_content_gap','resp_retransmitted_payload','resp_zero_window','orig_ack','orig_payload','orig_inconsistent','orig_multi_flag','resp_ack','resp_payload','resp_inconsistent','resp_multi_flag']
        #     self.__attr_to_xes_events = [attr for attr in self.__attr_to_xes_events if attr != self.__activity_attr]
        # else:
        #     self.__attr_to_xes_traces = ['orig_ip','orig_port','resp_ip','resp_port','proto','label']
        #     self.__attr_to_xes_events = ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes','orig_syn','orig_fin','orig_syn_ack','orig_rst','resp_syn','resp_fin','resp_syn_ack','resp_rst','orig_bad_checksum','orig_content_gap','orig_retransmitted_payload','orig_zero_window','resp_bad_checksum','resp_content_gap','resp_retransmitted_payload','resp_zero_window','orig_ack','orig_payload','orig_inconsistent','orig_multi_flag','resp_ack','resp_payload','resp_inconsistent','resp_multi_flag']
        #     self.__activity_attr = 'orig_syn'


    def execute_application(self) -> None:
        self.__train_model()
        self.__test_model()

    def __train_model():
        # TODO: eseguire il training
        pass

    def __test_model():
        # TODO: eseguire il testing 
        pass

main = MainMachineLearning('config.ini')