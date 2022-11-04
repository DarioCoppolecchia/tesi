from EntryPoint.MainTraceController import MainTraceController
from EntryPoint.MainMachineLearning import MainMachineLearning
import sys

if __name__ == "__main__":
    #try:
        operation = sys.argv[1]
        if operation == 'dataset':
            MainTraceController('config.ini')
        elif operation == 'ml':
            MainMachineLearning('config.ini')
        else:
            print('!!!!operation invalid!!!!\nvalid operations:\n- dataset\n- ml')
    #except:
    #    print('!!!!no operation selected!!!!\nvalid operations:\n- dataset\n- ml')