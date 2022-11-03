from EntryPoint.MainTraceController import MainTraceController
from EntryPoint.MainMachineLearning import MainMachineLearning
import sys

if __name__ == "__main__":
    print('modificato')
    input()
    operation = sys.argv[1]
    if operation == 'dataset':
        MainTraceController('config.ini')
    elif operation == 'ml':
        MainMachineLearning('config.ini')
    else:
        print('!!!!operation invalid!!!!\nvalid operations:\n- dataset\n- ml\n')