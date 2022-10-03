from ConnectionsModule.TracesController import TracesController
import os

class MainApplicationCLI:
    """
    Class that contains the UI and the startup routine of the application

    Args:
        config_path (str): if provided, the application loads the configuration options from the file at that path
    """
    def __init__(self, config_path: str = '') -> None:
        """Constructor of class Main

        :param config_path: if provided, the application loads the configuration options from the file at that path, defaults to ''
        :type config_path: str, optional
        """
        if config_path == '':
            config_path = input('type the path of the config.ini file\n> ')
        self.start_application(config_path)
        self.main_loop()

    def start_application(self, config_path: str = ''):
        """The routine of the startup of the class that consists in reading all the configuration options
        from the config file or from the user if the confi_path isn't given

        :param config_path: path of the configuration file, defaults to ''
        :type config_path: str, optional
        """
        self.traces_controller = TracesController()

        if config_path != '':
            self.traces_controller.load_paths_and_filters_from_config_file(config_path)
        else:
            print('path of the config file not given, enter config options manually:')
            self.traces_controller.strings_to_filter_event = self.__get_lines_from_input('the string to add to the list of strings to filter out')
            self.traces_controller.path_of_file_input = input('type the path of the file containing the lines of the connections to analyze\n> ')
            self.traces_controller.path_of_file_output = input('the path of the file that will contain the preprocessed lines (optional)\n> ')
            self.traces_controller.path_of_file_json = input('the path of the json file where to store the json of the list of NetworkConversation (optional)\n> ')
    
    def __cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_loop(self):
        """
        main loop of the application containig the UI elements that control the TracesController
        for every iteration this allows the user to do one of the following operations:
            #. Normalize lines and convert them to a Traces list
            #. print traces list to a json file
            #. exit program
        """
        while True:
            op = input("""\ntype the number for the various options:
    1) Normalize lines and convert them to a Traces list
    2) print traces list to a json file
    3) apply equal width discretization and print some trace
    4) apply equal height discretization and print some trace
    0) exit program\n> """)
            self.__cls()
            if op == "1":
                self.traces_controller.normalize_lines()
            elif op == "2":
                self.traces_controller.print_Trace_list_to_json_file()
            elif op == "3":
                self.__handle_attribute_discretization('equal_width')
            elif op == "4":
                self.__handle_attribute_discretization('equal_height')
            elif op == "0":
                res = input('are you sure you want to exit? (y or Y or just enter a blank line):\n> ')
                if res == '' or res.lower() == 'y':
                    return
            else:
                print('command not valid, enter an integer number between 1 and 3')
    
    def __input_attributes_and_n_bins_per_attribute(self):
        attr_bins_dict = {}
        attrs = [
            'orig_bytes',
            'resp_bytes',
            'missed_bytes',
            'orig_pkts',
            'duration',
            'orig_ip_bytes',
            'resp_pkts',
            'resp_ip_bytes',
        ]
        default_n = 10
        MAX_N_BINS = 5000
        while(True):
            res = input(f'''
current attribute selected:
    ''' + str('\n    '.join([str(element) for element in list(attr_bins_dict.items())])).translate(str.maketrans({"'": '', "(": '', ")": '', ",": ':', })) + 
f'''

Type the number of the attribute to discretize from the following list followed by the number of bins (if not specified, default is {default_n}):
''' + 
'\n'.join([f'    {element[0] + 1}) {element[1]}' for element in list(enumerate(attrs))]) + 
'''to apply discretization with these attribute type 0 or just enter (leave blank)
> ''')
            self.__cls()
            if res == '' or res == '0':
                if len(attr_bins_dict) == 0:
                    print('ERROR: at least one attribute must be selected')
                    continue
                else:
                    return attr_bins_dict
            ans = res.replace(' ', '').split(',')

            # check if the argument are 1 or 2
            if 1 <= len(ans) <= 2:
                # check if the first and second argument are numeric
                if len(ans) == 1:
                    ans += [str(default_n)]
                if ans[0].isnumeric() and ans[1].isnumeric():
                    # check if the first argument is in bounds
                    attr = int(ans[0])
                    n_bins = int(ans[1])
                    if attr in range(1, len(attrs) + 1):
                        if 1 < n_bins < MAX_N_BINS:
                            attr_bins_dict[attrs[attr]] = n_bins
                        else:
                            print(f'ERROR: the number of bins must be between 1 and {MAX_N_BINS}')
                    else:
                        print('ERROR: the value for the attribute isn\'t valid')
                else:
                    print('ERROR: the parameter must be number')
            else:
                print('ERROR: the number of parameter must be 1 or 2')
                
    def __handle_attribute_discretization(self, discretization: str='equal_width') -> None:
        attr_bins_dict = self.__input_attributes_and_n_bins_per_attribute()
        if discretization == 'equal_width':
            self.traces_controller.discretize_attributes_equal_width(attr_bins_dict)
        elif discretization == 'equal_height':
            self.traces_controller.discretize_attributes_equal_height(attr_bins_dict)
        else:
            raise ValueError('invalid discretization specified')
        for trace in self.traces_controller.get_n_traces_and_event():
            print(trace)
    
    def __get_lines_from_input(self, message: str) -> list:
        """returns a list filled from the std input and for each element of the list
        prints the message given as a parameter

        :param message: message to be displayed before each line of input
        :type message: str
        :return: list filled by the user via std input
        :rtype: list
        """
        lines = []
        while True:
            temp = input('type:\n- ' + message + ' or\n- END: to end the list\n> ')
            if temp == 'END':
                break
            else:
                lines.append(temp)
            
        os.system('cls' if os.name == 'nt' else 'clear')
        return lines