from MachineLearning.AnomalyDetector    import AnomalyDetector
from MachineLearning.PetriNetCollector  import PetriNetCollector
import pandas as pd

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
            attrs = attrs.split(',')
        else:
            attrs = ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','orig_syn','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes','orig_syn','orig_fin','orig_syn_ack','orig_rst','resp_syn','resp_fin','resp_syn_ack','resp_rst','orig_bad_checksum','orig_content_gap','orig_retransmitted_payload','orig_zero_window','resp_bad_checksum','resp_content_gap','resp_retransmitted_payload','resp_zero_window','orig_ack','orig_payload','orig_inconsistent','orig_multi_flag','resp_ack','resp_payload','resp_inconsistent','resp_multi_flag']

        self.__petriNetCollector = PetriNetCollector(attrs, delta)
        self.__anomalyDetector = AnomalyDetector()

    def execute_application(self, config_path: str='') -> None:
        self.__train_model(config_path)
        self.__test_model(config_path)

    def __train_model(self, config_path: str=''):
        import configparser

        config = configparser.ConfigParser()
        config.read(config_path)

        if 'Files' in config:
            path_of_file_xes_train = config['Files']['path_of_file_xes_train'] if 'path_of_file_xes_train' in config['Files'] else '../logs/ML/conn_train_pn.xes'
            path_of_petriNet_models_train = config['Files']['path_of_petriNet_models_train'] if 'path_of_petriNet_models_train' in config['Files'] else '../models/PetriNets/train/pn'
            path_of_anomalyDetector_models_train = config['Files']['path_of_anomalyDetector_models_train'] if 'path_of_anomalyDetector_models_train' in config['Files'] else '../models/anomalyDetector/anomalyDetector.model'
            path_of_petriNet_models_dataset_train = config['Files']['path_of_petriNet_models_dataset_train'] if 'path_of_petriNet_models_dataset_train' in config['Files'] else '../models/PetriNets/dataset_train/pn'
        else:
            path_of_file_xes_train = '../logs/ML/conn_train_pn.xes'
            path_of_petriNet_models_train = '../models/PetriNets/train/pn'
            path_of_anomalyDetector_models_train = '../models/anomalyDetector/anomalyDetector.model'
            path_of_petriNet_models_dataset_train = '../models/PetriNets/dataset_train/pn'

        path_of_file_xes_train_dataset = '../logs/ML/conn_train_dataset.xes'

        print('loading the xes train file...')
        self.__petriNetCollector.load_xes(path_of_file_xes_train)
        print('training the petriNet...')
        self.__petriNetCollector.train(path_of_petriNet_models_train)
        #print('loading the xes train file for dataset...')
        #self.__petriNetCollector.load_xes(path_of_file_xes_train_dataset)
        #print('creating the dataset for the Anomaly Detector...')
        #dataset, _ = self.__petriNetCollector.create_PetriNet_dataset(path_of_petriNet_models_dataset_train)
        #print('training the Anomaly Detector...')
        #self.__anomalyDetector.train(dataset, path_of_anomalyDetector_models_train)

    def __test_model(self, config_path: str=''):
        import configparser

        config = configparser.ConfigParser()
        config.read(config_path)

        if 'Files' in config:
            path_of_petriNet_models_dataset_test = config['Files']['path_of_petriNet_models_dataset_test'] if 'path_of_petriNet_models_dataset_test' in config['Files'] else '../models/PetriNets/dataset_test/pn'
            path_of_file_xes_test = config['Files']['path_of_file_xes_test'] if 'path_of_file_xes_test' in config['Files'] else '../logs/ML/conn_test.xes'

        else:
            path_of_petriNet_models_dataset_test = '../models/PetriNets/dataset_test/pn'
            path_of_file_xes_test = '../logs/ML/conn_test.xes'
        
        print('loading the xes test file...')
        self.__petriNetCollector.load_xes(path_of_file_xes_test)
        print('creating the dataset for the Anomaly Detector...')
        dataset, Y = self.__petriNetCollector.create_PetriNet_dataset(path_of_petriNet_models_dataset_test)
        dataset['label'] = Y
        dataset.to_csv('../models/PetriNets/dataset_test.csv')
        self.__gen_csv_pred_fittizia(dataset, Y, '../models/PetriNets/report.csv')
        #print('predicting with Anomaly Detector...')
        #y_pred = self.__anomalyDetector.predict(dataset)
        #for i in range(1, len(dataset.columns) + 1):
        #    y_pred = self.predizione(dataset, i)
        #    print(f'printing the results conf matrix {i}...')
        #    self.__anomalyDetector.create_confusion_matrix(Y, y_pred, i)

    def __getDFRow(self, soglia, crDict, cm):
        row = {}
        row['soglia'] = soglia
        row['TP'] = cm[1, 1]
        row['FN'] = cm[1, 0]
        row['FP'] = cm[0, 1]
        row['TN'] = cm[0, 0]
        row['precision (positive)'] = crDict['1']['precision']
        row['recall (positive)'] = crDict['1']['recall']
        row['fscore (positive)'] = crDict['1']['f1-score']
        row['precision (negative)'] = crDict['-1']['precision']
        row['recall (negative)'] = crDict['-1']['recall']
        row['fscore (negative)'] = crDict['-1']['f1-score']
        row['accuracy'] = crDict['accuracy']
        row['macroF'] = crDict['macro avg']['f1-score']
        row['WeigthedF'] = crDict['weighted avg']['f1-score']
        return row
    
    def __gen_csv_pred_fittizia(self, X, Y, file_name_out):
        import matplotlib.pyplot as plt
        from tqdm import tqdm
        from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

        report = []
        for i in tqdm(range(1, len(X.columns) + 1)):
            y_pred = self.__prediction(X, i)
            cr = classification_report(Y, y_pred, output_dict=True)
            cm = confusion_matrix(Y, y_pred)
            cm_display = ConfusionMatrixDisplay(confusion_matrix = cm)
            cm_display.plot()
            plt.show()
            report.append(self.__getDFRow(i, cr, cm))
        pd.DataFrame(report).to_csv(file_name_out)

    def __prediction(self, X: pd.DataFrame, soglia: int):
        y_pred = []
        for _, x in X.iterrows():
            if sum([1 if attr != 1 else 0 for attr in x]) >= soglia:
                y_pred.append(-1)
            else:
                y_pred.append(1)
        return y_pred
