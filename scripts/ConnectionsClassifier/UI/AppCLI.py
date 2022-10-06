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
        import configparser
        self.traces_controller = TracesController()
        self.traces_controller.load_paths_and_filters_from_config_file(config_path)

        config = configparser.ConfigParser()
        config.read(config_path)

        # checks if Discretization is in config.ini file
        if 'Discretization' in config:
            type = config['Discretization']['discretization_type'] if 'discretization_type' in config['Discretization'] else 'equal_frequency'
            self.__discretization_type = DISCRETIZATION_TYPE.EQUAL_FREQUENCY if type == 'equal_frequency' else DISCRETIZATION_TYPE.EQUAL_WIDTH
        else:
            self.__discretization_type = DISCRETIZATION_TYPE.EQUAL_FREQUENCY

        if 'Attributes' in config:
            attr_2_disc = config['Attributes']['attributes_to_discretize'].split(',') if 'attributes_to_discretize' in config['Attributes'] else ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes']
            n_bins = [int(bin) for bin in config['Attributes']['n_bins'].split(',')] if 'n_bins' in config['Attributes'] else [10 for _ in attr_2_disc]
            if len(attr_2_disc) != len(n_bins):
                raise ValueError('The length of the attributes to discretize don\it match with the length of the number of bins')
            else:
                self.__attr_bins_dict = dict(zip(attr_2_disc, n_bins))
            self.__attr_to_xes = config['Attributes']['attributes_to_xes'].split(',') if 'attributes_to_xes' in config['Attributes'] else ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','history','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes']
        else:
            attr_2_disc = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes']
            n_bins = [10 for _ in attr_2_disc]
            self.__attr_bins_dict = dict(zip(attr_2_disc, n_bins))
            self.__attr_to_xes = ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','history','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes']

        if 'Print' in config:
            self.__n_trace_to_print = int(config['Print']['n_trace_to_print']) if 'n_trace_to_print' in config['Print'] else 10
            self.__randomize_print = bool(config['Print']['randomize_print']) if 'randomize_print' in config['Print'] else True
        else:
            self.__n_trace_to_print = 10
            self.__randomize_print = True
    
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
        self.__cls()
        self.traces_controller.read_and_convert_lines()
        #self.traces_controller.print_Trace_list_to_xes_file()
        self.__print_n_traces_and_events()
        self.__handle_attribute_discretization()
        self.__print_n_discretized_traces_and_events()
    
    def __print_n_traces_and_events(self) -> None:
        """prints n random or non random traces and all the events of those traces
        """
        for trace in self.traces_controller.get_n_traces_and_event(max_n_trace=self.__n_trace_to_print, randomize=self.__randomize_print):
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
                
    def __handle_attribute_discretization(self) -> None:
        """applies discretization algorithm based on the parameter's value

        :param discretization: discretization algorithm to use, defaults to 'equal_width'
        :type discretization: str, optional
        :raises ValueError: if the discretization algorithm isn't equal_width or equal_height, a ValueError will be thrown
        """
        self.traces_controller.discretize_attributes(self.__discretization_type, self.__attr_bins_dict)
        self.__print_n_discretized_traces_and_events()