import os
from ConnectionsModule.TracesController     import TracesController
from ConnectionsModule.Event                import Event
from ConnectionsModule.CONN_LABEL           import CONN_LABEL
from ConnectionsModule.CONN_STATE           import CONN_STATE
from ConnectionsModule.PROTO                import PROTO
from DiscretizerModule.DISCRETIZATION_TYPE  import DISCRETIZATION_TYPE
from ConnectionsModule.EventHistory         import EventHistory

class MainTraceController:
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
        self.execute_application()

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

        n_bins = 10
        # checks if Discretization is in config.ini file
        if 'Discretization' in config:
            type = config['Discretization']['discretization_type'] if 'discretization_type' in config['Discretization'] else 'equal_frequency'
            self.__discretization_type = DISCRETIZATION_TYPE.EQUAL_FREQUENCY if type == 'equal_frequency' else DISCRETIZATION_TYPE.EQUAL_WIDTH
            n_bins = int(config['Discretization']['n_bins']) if 'n_bins' in config['Discretization'] else n_bins
            soglia = int(config['Discretization']['soglia']) if 'soglia' in config['Discretization'] else soglia
        else:
            self.__discretization_type = DISCRETIZATION_TYPE.EQUAL_FREQUENCY
            n_bins = 5
            soglia = 10

        if 'Attributes' in config:
            self.__attr_to_xes_traces = config['Attributes']['attributes_to_xes_traces'].split(',') if 'attributes_to_xes_traces' in config['Attributes'] else ['orig_ip','orig_port','resp_ip','resp_port','proto','label']
            self.__attr_to_xes_events = config['Attributes']['attributes_to_xes_events'].split(',') if 'attributes_to_xes_events' in config['Attributes'] else ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes','orig_syn','orig_fin','orig_syn_ack','orig_rst','resp_syn','resp_fin','resp_syn_ack','resp_rst','orig_bad_checksum','orig_content_gap','orig_retransmitted_payload','orig_zero_window','resp_bad_checksum','resp_content_gap','resp_retransmitted_payload','resp_zero_window','orig_ack','orig_payload','orig_inconsistent','orig_multi_flag','resp_ack','resp_payload','resp_inconsistent','resp_multi_flag']
        else:
            self.__attr_to_xes_traces = ['orig_ip','orig_port','resp_ip','resp_port','proto','label']
            self.__attr_to_xes_events = ['ts','service','duration','orig_bytes','resp_bytes','conn_state','missed_bytes','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes','orig_syn','orig_fin','orig_syn_ack','orig_rst','resp_syn','resp_fin','resp_syn_ack','resp_rst','orig_bad_checksum','orig_content_gap','orig_retransmitted_payload','orig_zero_window','resp_bad_checksum','resp_content_gap','resp_retransmitted_payload','resp_zero_window','orig_ack','orig_payload','orig_inconsistent','orig_multi_flag','resp_ack','resp_payload','resp_inconsistent','resp_multi_flag']

        discretizable_attrs = {
            'orig_bytes',
            'resp_bytes',
            'missed_bytes',
            'orig_pkts',
            'duration',
            'orig_ip_bytes',
            'resp_pkts',
            'resp_ip_bytes',
            'orig_syn',
            'orig_fin',
            'orig_syn_ack',
            'orig_rst',
            'resp_syn',
            'resp_fin',
            'resp_syn_ack',
            'resp_rst',
            'orig_bad_checksum',
            'orig_content_gap',
            'orig_retransmitted_payload',
            'orig_zero_window',
            'resp_bad_checksum',
            'resp_content_gap',
            'resp_retransmitted_payload',
            'resp_zero_window',
        }
        attr_to_discretize = list(set(self.__attr_to_xes_events).intersection(discretizable_attrs))
        bins_list = [n_bins for _ in range(len(attr_to_discretize))]
        soglia_list = [soglia for _ in range(len(attr_to_discretize))]
        self.__attr_bins_dict = dict(zip(attr_to_discretize, zip(bins_list, soglia_list)))

        if 'Print' in config:
            self.__show_examples = bool(int(config['Print']['show_examples'])) if 'show_examples' in config['Print'] else True
            self.__n_trace_to_print = int(config['Print']['n_trace_to_print']) if 'n_trace_to_print' in config['Print'] else 10
            self.__randomize_print = bool(int(config['Print']['randomize_print'])) if 'randomize_print' in config['Print'] else True
        else:
            self.__show_examples = True
            self.__n_trace_to_print = 10
            self.__randomize_print = True
    
    def __cls(self) -> None:
        """clears the screen on either windows or non windows system
        """        
        os.system('cls' if os.name == 'nt' else 'clear')

    def execute_application(self) -> None:
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
        self.__print_n_traces_and_events() if self.__show_examples else ''
        self.traces_controller.discretize_attributes(self.__discretization_type, self.__attr_bins_dict)
        self.__print_n_discretized_traces_and_events() if self.__show_examples else ''
        self.traces_controller.print_Trace_list_to_xes_file(self.__attr_to_xes_traces, self.__attr_to_xes_events)
    
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
        
        if EventHistory.disc_orig_syn is not None:
            print(f'originator syn discretization:\n\tnumber of bins: {EventHistory.disc_orig_syn.get_n_bins()}\n\tbins: {EventHistory.disc_orig_syn.get_discretized_bins()}')
        if EventHistory.disc_orig_fin is not None:
            print(f'originator fin discretization:\n\tnumber of bins: {EventHistory.disc_orig_fin.get_n_bins()}\n\tbins: {EventHistory.disc_orig_fin.get_discretized_bins()}')
        if EventHistory.disc_orig_syn_ack is not None:
            print(f'originator syn-ack discretization:\n\tnumber of bins: {EventHistory.disc_orig_syn_ack.get_n_bins()}\n\tbins: {EventHistory.disc_orig_syn_ack.get_discretized_bins()}')
        if EventHistory.disc_orig_rst is not None:
            print(f'originator rst discretization:\n\tnumber of bins: {EventHistory.disc_orig_rst.get_n_bins()}\n\tbins: {EventHistory.disc_orig_rst.get_discretized_bins()}')
        if EventHistory.disc_resp_syn is not None:
            print(f'responder syn discretization:\n\tnumber of bins: {EventHistory.disc_resp_syn.get_n_bins()}\n\tbins: {EventHistory.disc_resp_syn.get_discretized_bins()}')
        if EventHistory.disc_resp_fin is not None:
            print(f'responder fin discretization:\n\tnumber of bins: {EventHistory.disc_resp_fin.get_n_bins()}\n\tbins: {EventHistory.disc_resp_fin.get_discretized_bins()}')
        if EventHistory.disc_resp_syn_ack is not None:
            print(f'responder syn-ack discretization:\n\tnumber of bins: {EventHistory.disc_resp_syn_ack.get_n_bins()}\n\tbins: {EventHistory.disc_resp_syn_ack.get_discretized_bins()}')
        if EventHistory.disc_resp_rst is not None:
            print(f'responder rst discretization:\n\tnumber of bins: {EventHistory.disc_resp_rst.get_n_bins()}\n\tbins: {EventHistory.disc_resp_rst.get_discretized_bins()}')
        if EventHistory.disc_orig_bad_checksum is not None:
            print(f'originator bad checksum discretization:\n\tnumber of bins: {EventHistory.disc_orig_bad_checksum.get_n_bins()}\n\tbins: {EventHistory.disc_orig_bad_checksum.get_discretized_bins()}')
        if EventHistory.disc_orig_content_gap is not None:
            print(f'originator content gap discretization:\n\tnumber of bins: {EventHistory.disc_orig_content_gap.get_n_bins()}\n\tbins: {EventHistory.disc_orig_content_gap.get_discretized_bins()}')
        if EventHistory.disc_orig_retransmitted_payload is not None:
            print(f'originator retransmitted payload discretization:\n\tnumber of bins: {EventHistory.disc_orig_retransmitted_payload.get_n_bins()}\n\tbins: {EventHistory.disc_orig_retransmitted_payload.get_discretized_bins()}')
        if EventHistory.disc_orig_zero_window is not None:
            print(f'originator zero window discretization:\n\tnumber of bins: {EventHistory.disc_orig_zero_window.get_n_bins()}\n\tbins: {EventHistory.disc_orig_zero_window.get_discretized_bins()}')
        if EventHistory.disc_resp_bad_checksum is not None:
            print(f'responder bad checksum discretization:\n\tnumber of bins: {EventHistory.disc_resp_bad_checksum.get_n_bins()}\n\tbins: {EventHistory.disc_resp_bad_checksum.get_discretized_bins()}')
        if EventHistory.disc_resp_content_gap is not None:
            print(f'responder content gap discretization:\n\tnumber of bins: {EventHistory.disc_resp_content_gap.get_n_bins()}\n\tbins: {EventHistory.disc_resp_content_gap.get_discretized_bins()}')
        if EventHistory.disc_resp_retransmitted_payload is not None:
            print(f'responder retransmitted payload discretization:\n\tnumber of bins: {EventHistory.disc_resp_retransmitted_payload.get_n_bins()}\n\tbins: {EventHistory.disc_resp_retransmitted_payload.get_discretized_bins()}')
        if EventHistory.disc_resp_zero_window is not None:
            print(f'responder zero window discretization:\n\tnumber of bins: {EventHistory.disc_resp_zero_window.get_n_bins()}\n\tbins: {EventHistory.disc_resp_zero_window.get_discretized_bins()}')

        for trace in self.traces_controller.get_n_traces_and_event(randomize=True):
            print(f'''
traces of connection {trace.get_orig_ip()}:{trace.get_orig_port()} {trace.get_resp_ip()}:{trace.get_resp_port()}
with protocol: {PROTO.proto_to_str(trace.get_proto())}
first packet sent in: {datetime.fromtimestamp(float(trace.get_ts_on_open()))}
with label: {CONN_LABEL.conn_label_to_str(trace.get_label())}
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

        '''
        from collections import Counter, OrderedDict
        redundant_dict = {}

        disc_bins = Event.disc_orig_bytes.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_bytes')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_bytes'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_bytes'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = Event.disc_resp_bytes.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_bytes')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_bytes'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_bytes'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = Event.disc_missed_bytes.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('missed_bytes')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['missed_bytes'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['missed_bytes'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': group_by_occ(OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True))),
            }
        
        disc_bins = Event.disc_orig_pkts.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_pkts')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_pkts'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_pkts'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = Event.disc_duration.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('duration')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['duration'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['duration'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = Event.disc_orig_ip_bytes.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_ip_bytes')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_ip_bytes'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_ip_bytes'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = Event.disc_resp_pkts.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_pkts')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_pkts'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_pkts'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = Event.disc_resp_ip_bytes.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_ip_bytes')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_ip_bytes'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_ip_bytes'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_orig_syn.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_syn')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_syn'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_syn'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_orig_fin.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_fin')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_fin'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_fin'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_orig_syn_ack.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_syn_ack')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_syn_ack'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_syn_ack'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_orig_rst.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_rst')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_rst'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_rst'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_resp_syn.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_syn')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_syn'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_syn'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_resp_fin.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_fin')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_fin'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_fin'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_resp_syn_ack.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_syn_ack')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_syn_ack'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_syn_ack'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_resp_rst.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_rst')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_rst'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_rst'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_orig_bad_checksum.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_bad_checksum')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_bad_checksum'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_bad_checksum'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_orig_content_gap.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_content_gap')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_content_gap'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_content_gap'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_orig_retransmitted_payload.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_retransmitted_payload')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_retransmitted_payload'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_retransmitted_payload'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_orig_zero_window.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('orig_zero_window')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['orig_zero_window'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['orig_zero_window'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_resp_bad_checksum.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_bad_checksum')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_bad_checksum'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_bad_checksum'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_resp_content_gap.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_content_gap')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_content_gap'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_content_gap'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_resp_retransmitted_payload.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_retransmitted_payload')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_retransmitted_payload'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_retransmitted_payload'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        
        disc_bins = EventHistory.disc_resp_zero_window.get_discretized_bins()
        attr_list = self.traces_controller.get_list_of_attribute('resp_zero_window')
        if 'soglia' == disc_bins[-1]:
            disc_bins.remove('soglia')
            redundant_dict['resp_zero_window'] = {
                'motivo per essere loggato': 'inferiore a max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }
        elif 'con duplicati' == disc_bins[-1]:
            disc_bins.remove('con duplicati')
            redundant_dict['resp_zero_window'] = {
                'motivo per essere loggato': 'sono presenti duplicati anche se maggiore di max{soglia, n_bins}', 
                'bins discretizzati': disc_bins, 
                'occorrenza valori': OrderedDict(sorted(Counter(attr_list).items(), key=lambda row: row[1], reverse=True)),
            }

        from matplotlib import pyplot as plt
        import numpy as np

        with open('attribute_bins_and_number_of_occurrencies.json', 'w') as f:
            f.write(to_json(redundant_dict, 20))

        for attr, arr in redundant_dict.items():
            x = np.array([val for val in arr[1].keys()])
            y = np.array([val for val in arr[1].values()])

            plt.xlabel('valore')
            plt.ylabel('occorrenza valore')
            plt.title(f'values occurrencies for {attr} attribute')
            plt.scatter(x, y)
            plt.grid()
            plt.show()
        '''

main = MainTraceController('config.ini')