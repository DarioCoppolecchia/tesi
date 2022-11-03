from EntryPoint.MainTraceController import MainTraceController
from EntryPoint.MainMachineLearning import MainMachineLearning
import sys

if __name__ == "__main__":
    # TODO: da fixare il fatto che non sembra essersi aggiornato
    operation = sys.argv[1]
    if operation == 'dataset':
        MainMachineLearning('config.ini')
    elif operation == 'ml':
        MainTraceController('config.ini')
    else:
        print('!!!!operation invalid!!!!\nvalid operations:\n- dataset\n- ml\n')