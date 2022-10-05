import os
from ConnectionsModule.TracesController     import TracesController
from ConnectionsModule.Event                import Event
from ConnectionsModule.CONN_STATE           import CONN_STATE
from DiscretizerModule.DISCRETIZATION_TYPE  import DISCRETIZATION_TYPE

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
    
    def __cls(self) -> None:
        """clears the screen on either windows or non windows system
        """        
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_loop(self) -> None:
        """
        main loop of the application containig the UI elements that control the TracesController
        for every iteration this allows the user to do one of the following operations:
            #. Read network data and convert them to a Traces list
            #. print traces list to a json file
            #. apply equal width discretization and print some trace
            #. apply equal height discretization and print some trace
            #. print N traces and events
            #. print N discretized traces and events
            #. exit program
        """
        while True:
            op = input("""\ntype the number for the various options:
    1) Read network data and convert them to a Traces list
    2) print traces list to a json file
    3) apply equal width discretization and print some trace
    4) apply equal height discretization and print some trace
    5) print N traces and events
    6) print N discretized traces and events
    0) exit program\n> """)
            self.__cls()
            if op == "1":
                self.traces_controller.read_and_convert_lines()
            elif op == "2":
                self.traces_controller.print_Trace_list_to_xes_file()
            elif op == "5":
                self.__print_n_traces_and_events()
            elif op == "6":
                self.__print_n_discretized_traces_and_events()
            elif op == "0":
                res = input('are you sure you want to exit? (y or Y or just enter a blank line):\n> ')
                if res == '' or res.lower() == 'y':
                    return
            else:
                print('command not valid, enter an integer number between 1 and 3')
    
    def __input_attributes_and_n_bins_per_attribute(self) -> None:
        """This method let's the user choose what attribute to discretize and with how many bins
        """        
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
'''
to apply discretization with these attribute type 0 or just enter (leave blank)
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
                            attr_bins_dict[attrs[attr - 1]] = n_bins
                        else:
                            print(f'ERROR: the number of bins must be between 1 and {MAX_N_BINS}')
                    else:
                        print('ERROR: the value for the attribute isn\'t valid')
                else:
                    print('ERROR: the parameter must be number')
            else:
                print('ERROR: the number of parameter must be 1 or 2')
    
    def __print_n_traces_and_events(self) -> None:
        """prints n random or non random traces and all the events of those traces
        """        
        n = 0
        randomize = False
        while(True):
            ans = input('Type the number of traces to print: ')
            if ans.isdigit():
                n = int(ans)
                if n <= 0:
                    print('ERROR: number of traces to print must be greater than 0')
                else:
                    break
            else:
                print('ERROR: invalid integer')
        while(True):
            ans = input(f'Do you want to print random traces? (y, Y or "enter" for yes; n or N for the first {n} traces)')
            if ans == 'y' or ans == 'Y' or ans == '':
                randomize = True
                break
            elif ans == 'n' or ans == 'N':
                randomize = False
                break
            else:
                print('ERROR: value entered not valid')
        for trace in self.traces_controller.get_n_traces_and_event(max_n_trace=n, randomize=randomize):
            print(trace)

    def __print_n_discretized_traces_and_events(self) -> None:
        """prints the characteristics of the discretization algorithms (n bins and the bins) and some traces with their respective events
        """        
        from datetime import datetime
        # printing the bins
        if Event.disc_duration is not None:
            print(f'duration discretization:\n\tnumber of bins: {Event.disc_duration.get_n_bins()}\n\tbins: {Event.disc_duration.get_discretized_bins()}')
        if Event.disc_orig_bytes is not None:
            print(f'origin bytes discretization :\n\tnumber of bins: {Event.disc_orig_bytes.get_n_bins()}\n\tbins: {Event.disc_orig_bytes.get_discretized_bins()}')
        if Event.disc_resp_bytes is not None:
            print(f'responder bytes discretization:\n\tnumber of bins: {Event.disc_resp_bytes.get_n_bins()}\n\tbins: {Event.disc_resp_bytes.get_discretized_bins()}')
        if Event.disc_missed_bytes is not None:
            print(f'missed bytes discretization:\n\tnumber of bins: {Event.disc_missed_bytes.get_n_bins()}\n\tbins: {Event.disc_missed_bytes.get_discretized_bins()}')
        if Event.disc_orig_pkts is not None:
            print(f'origin packets discretization:\n\tnumber of bins: {Event.disc_orig_pkts.get_n_bins()}\n\tbins: {Event.disc_orig_pkts.get_discretized_bins()}')
        if Event.disc_orig_ip_bytes is not None:
            print(f'origin bytes ip protocol discretization:\n\tnumber of bins: {Event.disc_orig_ip_bytes.get_n_bins()}\n\tbins: {Event.disc_orig_ip_bytes.get_discretized_bins()}')
        if Event.disc_resp_pkts is not None:
            print(f'responder packets discretization:\n\tnumber of bins: {Event.disc_resp_pkts.get_n_bins()}\n\tbins: {Event.disc_resp_pkts.get_discretized_bins()}')
        if Event.disc_resp_ip_bytes is not None:
            print(f'responder bytes ip discretization:\n\tnumber of bins: {Event.disc_resp_ip_bytes.get_n_bins()}\n\tbins: {Event.disc_resp_ip_bytes.get_discretized_bins()}')

        for trace in self.traces_controller.get_n_traces_and_event(randomize=True):
            print(f'''
traces of connection {trace.get_orig_ip()}:{trace.get_orig_port()} {trace.get_resp_ip()}:{trace.get_resp_port()}
with protocol: {trace.get_proto()}
first packet sent in: {datetime.fromtimestamp(float(trace.get_ts_on_open()))}
with label: {trace.get_label()}
''')
            for event in trace.get_events():
                print(f'''    connection created at {datetime.fromtimestamp(float(event.get_ts()))}
    using the {event.get_service()} service
    lasted {event.get_discretized_duration()} seconds
    the originator sent {event.get_discretized_orig_bytes()} and the responder sent {event.get_discretized_resp_bytes()}
    the state of the connection is {CONN_STATE.state_to_str(event.get_conn_state())}
    {event.get_discretized_missed_bytes()} bytes were missed during the lifetime of this connection
    the history of this connection is {event.get_history().get_history()}
    the orginator sent {event.get_discretized_orig_pkts()} ({event.get_discretized_orig_ip_bytes()} bytes in the packet header)
    the orginator sent {event.get_discretized_resp_pkts()} ({event.get_discretized_resp_ip_bytes()} bytes in the packet header)
''')
                
    def __handle_attribute_discretization(self, discretization: DISCRETIZATION_TYPE=DISCRETIZATION_TYPE.EQUAL_FREQUENCY) -> None:
        """applies discretization algorithm based on the parameter's value

        :param discretization: discretization algorithm to use, defaults to 'equal_width'
        :type discretization: str, optional
        :raises ValueError: if the discretization algorithm isn't equal_width or equal_height, a ValueError will be thrown
        """        
        attr_bins_dict = self.__input_attributes_and_n_bins_per_attribute()
        if discretization == DISCRETIZATION_TYPE.EQUAL_WIDTH:
            self.traces_controller.discretize_attributes_equal_width(attr_bins_dict)
        elif discretization == DISCRETIZATION_TYPE.EQUAL_FREQUENCY:
            self.traces_controller.discretize_attributes_equal_height(attr_bins_dict)
        else:
            raise ValueError('invalid specified discretization method')
        self.__print_n_discretized_traces_and_events()
    
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