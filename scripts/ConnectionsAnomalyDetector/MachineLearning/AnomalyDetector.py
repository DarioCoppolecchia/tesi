import pandas as pd
#import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.metrics import classification_report, confusion_matrix#, ConfusionMatrixDisplay

class AnomalyDetector:
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
    
    def generate_predictions(self, X, Y, file_name_out):

        report = []
        for i in tqdm(range(1, len(X.columns) + 1)):
            y_pred = self.__prediction(X, i)
            cr = classification_report(Y, y_pred, output_dict=True)
            cm = confusion_matrix(Y, y_pred)
            #cm_display = ConfusionMatrixDisplay(confusion_matrix = cm)
            #cm_display.plot()
            #plt.show()
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
