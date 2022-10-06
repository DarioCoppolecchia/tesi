from .Trace import Trace
from .Event import Event
from DiscretizerModule.Equal_Frequency_Discretizer import Equal_Frequency_Discretizer
from DiscretizerModule.Equal_Width_Discretizer import Equal_Width_Discretizer

class TracesController:
    """
    Class that contains the method used to filter and organize events and traces

    :param path_of_file_input: path of the file that contains the logs to be acquired
    :type path_of_file_input: str
    :param path_of_file_output: path of the file where the preprocessed lines are stored or will be stored
    :type path_of_file_output: str
    :param path_of_file_xes: path of the file where to write the xes file
    :type path_of_file_xes: str
    :param lines_to_remove_ash: set of the # to remove from the file
    :type lines_to_remove_ash: set[str]
    :param strings_to_filter_event: set of string to be filtered out
    :type strings_to_filter_event: set[str]
    :param network_traffic: list of the Trace
    :type network_traffic: list[Trace]
    :param traces_pos_dict: dict that contains the indices of network_traffic
    :type traces_pos_dict: dict{str: int}
    """
    def __init__(self, 
        path_of_file_input: str='',
        path_of_file_xes: str='',
        strings_to_filter_event: set=set()) -> None:
        """Constructor method

        :param path_of_file_input: path of the file from where to get the events, defaults to ''
        :type path_of_file_input: str, optional
        :param path_of_file_output: path of the file where to store the preprocessed lines, defaults to ''
        :type path_of_file_output: str, optional
        :param path_of_file_xes: path of the file where to dump the traces converted to xes, defaults to ''
        :type path_of_file_xes: str, optional
        :param lines_to_remove_ash: set of the strings that if match the start of a line in the input file, that substring will be removed (this doesn't delete it from the input file), defaults to set()
        :type lines_to_remove_ash: set, optional
        :param strings_to_filter_event: set of the substring to be removed from the lines read in the file (this doesn't delete it from the input file), defaults to set()
        :type strings_to_filter_event: set, optional
        """
        self.__path_of_file_input = path_of_file_input
        self.__path_of_file_xes = path_of_file_xes
        self.__strings_to_filter_event = strings_to_filter_event
        self.__network_traffic = []
        self.__traces_pos_dict = {}
    
    def load_paths_and_filters_from_config_file(self, config_file_path: str) -> None:
        """
        Loads all path and filters form the .ini file

        :param config_file_path: path of the configuration path
        :type config_file_path: str
        """   
        import configparser
        print('reading config option from file...')
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # checks if Files is in config.ini file
        if 'Files' in config:
            self.__path_of_file_input = config['Files']['path_of_file_input'] if 'path_of_file_input' in config['Files'] else ''
            self.__path_of_file_xes = config['Files']['path_of_file_xes']  if 'path_of_file_xes' in config['Files'] else ''
        else:
            self.__path_of_file_input = self.__path_of_file_input if self.__path_of_file_input != '' else ''
            self.__path_of_file_xes = self.__path_of_file_xes if self.__path_of_file_xes != '' else ''

        # checks if Filters is in config.ini file
        if 'Filters' in config:
            self.__strings_to_filter_event = config['Filters']['strings_to_filter_event']  if 'strings_to_filter_event' in config['Filters'] else ''
            self.__strings_to_filter_event = self.__strings_to_filter_event.replace('\'', '').split(',')
        else:
            self.__strings_to_filter_event = '' 

        print('...reading complete')

    def get_network_traffic(self) -> list:
        """returns the list of all the traces processed

        :return: the list of traces
        :rtype: list
        """        
        return self.__network_traffic

    def get_n_traces_and_event(self, max_n_trace: int=10, randomize: bool=False) -> list:
        """returns n traces random or non random and their respective events

        :param max_n_trace: number of traces to return, defaults to 10
        :type max_n_trace: int, optional
        :param randomize: set to true if the traces will be taken at random from network traffic, defaults to False
        :type randomize: bool, optional
        :return: the list of n traces
        :rtype: list
        """        
        from random import sample
        return sample(self.__network_traffic, max_n_trace) if randomize else self.__network_traffic[:10]

    def read_and_convert_lines(self):
        """
        read lines from file and converting them to a list of trace (network_traffic field)
        """
        print('normalizing and converting lines...')
        # normalizing lines
        with open(self.__path_of_file_input, "r") as f_in:
            lines_to_remove = [
                '#separator',
                '#set_separator',
                '#empty_field',
                '#unset_field',
                '#path',
                '#open',
                '#types',
                '#fields',
                '#close',
            ]
            next(f_in)
            for line in f_in:
                # removing comment lines
                for line_to_check in lines_to_remove:
                    if line.startswith(line_to_check):
                        break
                else:
                    # removing unnecessary sub strings
                    for string in self.__strings_to_filter_event:
                        line = line.replace(string, '')
                    self.conv_line_and_add_to_trace(line.replace('\n', ''))
        print('...normalization and conversion completed')

    def conv_line_and_add_to_trace(self, line: str):
        """
        Convert a preprocessed line from the input file to an event and adds it to the network_traffic list

        :param line: line of the event to be processed and added to a trace
        :type line: str
        """
        list_to_pack = line.split('\t')

        ts = list_to_pack[0]
        orig_ip = list_to_pack[2]
        orig_port = list_to_pack[3]
        resp_ip = list_to_pack[4]
        resp_port = list_to_pack[5]
        proto = list_to_pack[6]
        service = list_to_pack[7]
        duration = list_to_pack[8]
        orig_bytes = list_to_pack[9]
        resp_bytes = list_to_pack[10]
        conn_state = list_to_pack[11]
        missed_bytes = list_to_pack[14]
        history = list_to_pack[15]
        orig_pkts = list_to_pack[16]
        orig_ip_bytes = list_to_pack[17]
        resp_pkts = list_to_pack[18]
        resp_ip_bytes = list_to_pack[19]
        label = list_to_pack[21]

        event = Event(ts,
            service,
            duration,
            orig_bytes,
            resp_bytes,
            conn_state,
            missed_bytes,
            history,
            orig_pkts,
            orig_ip_bytes,
            resp_pkts,
            resp_ip_bytes)
    
        id = Trace.generate_id_static(orig_ip, orig_port, resp_ip, resp_port, proto)

        try:
            self.__network_traffic[self.__traces_pos_dict[id]].add_event(event)
        except KeyError:
            self.__traces_pos_dict[id] = len(self.__network_traffic)
            self.__network_traffic.append(Trace(orig_ip, orig_port, resp_ip, resp_port, proto, ts, label))
            self.__network_traffic[-1].add_event(event)
            
    
    
    '''
    def apply_label_to_events_in_file(self, constraint_to_label: list) -> None:
        """
        this function applies the label according by the rules in the parameter. The constraints must have timestamp upper bound and lower bound, ip of the attacker, ip of the attacked and the label. If the row doesn't follow the constraint, the label will be BENIGN

        The rules are described as follows
        :math:`label(x) <- 
            | lower_bound <= x.ts <= upper_bound && 
            | ip_attacker = x.ip_orig && 
            | ip_attacked = x.ip_resp`

        The structure of the constraint will be a list of dict, where the keys will be 
            * lower_bound, 
            * upper_bound, 
            * ip_attacker, 
            * ip_attacked, 
            * label
        and the values will be the corresponding values

        An example of the structure
        | interval_to_label = [
        |     { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
        |     { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
        |     ...
        |     { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
        | ]

        :param constraint_to_label: constraint to follow to apply the label correctly
        :type constraint_to_label: list
        """
        print('applying label to the file...')
        file = self.__path_of_file_input.replace('_labeled', '')
        with open(file, 'r') as f:
            lines = f.readlines()
            del lines[:6]
            del lines[1]
            del lines[-1]
            lines[0] = lines[0].replace("#fields\t", "")
        with open(file, 'w') as f:
            f.writelines(lines)
        with open(self.__path_of_file_input, 'w') as f_out:
            with open(file, 'r') as f_in:
                next(f_in)
                for line in f_in:
                    line = line.replace('\n', '')
                    splitted = line.split('\t')
                    ts = splitted[0]
                    orig_ip = splitted[2]
                    resp_ip = splitted[4]
                    for constraints in constraint_to_label:
                        if (float(constraints['lower_bound']) <= float(ts) <= float(constraints['upper_bound']) and
                            constraints['ip_attacker'] == orig_ip and
                            constraints['ip_attacked'] == resp_ip):
                            line += '\t' + constraints['label']
                            break
                    else:
                        line += '\t' + 'BENIGN'
                    f_out.write(line + '\n')
        print('...label application completed')
    '''
        
    def print_Trace_list_to_xes_file(self) -> None:
        """prints all the Traces list to a xes file
        """
        # TODO
        print('writing the list of Traces to a xes file...')
        pass

    def __get_list_of_all_attributes(self, attributes_to_discretize: set) -> dict:
        """Creates a dictionary of list of the values of each attribute

        Possible values of the attributes_to_discretize:
            #. orig_bytes
            #. resp_bytes
            #. missed_bytes
            #. orig_pkts
            #. duration
            #. orig_ip_bytes
            #. resp_pkts
            #. resp_ip_bytes

        :param attributes_to_discretize: list of the attributes from where to collect data from
        :type attributes_to_discretize: list
        :return: dictionary of list of the attributes of all item
        :rtype: dict
        """

        attributes_value_dict = {}
        for attribute in attributes_to_discretize:
            attributes_value_dict[attribute] = []

        # getting all value for each key of the dict
        if 'orig_bytes' in attributes_value_dict:
            attributes_value_dict['orig_bytes'] = [trace.get_list_of_orig_bytes() for trace in self.__network_traffic]
        if 'resp_bytes' in attributes_value_dict:
            attributes_value_dict['resp_bytes'] = [trace.get_list_of_resp_bytes() for trace in self.__network_traffic]
        if 'missed_bytes' in attributes_value_dict:
            attributes_value_dict['missed_bytes'] = [trace.get_list_of_missed_bytes() for trace in self.__network_traffic]
        if 'orig_pkts' in attributes_value_dict:
            attributes_value_dict['orig_pkts'] = [trace.get_list_of_orig_pkts() for trace in self.__network_traffic]
        if 'duration' in attributes_value_dict:
            attributes_value_dict['duration'] = [trace.get_list_of_duration() for trace in self.__network_traffic]
        if 'orig_ip_bytes' in attributes_value_dict:
            attributes_value_dict['orig_ip_bytes'] = [trace.get_list_of_orig_ip_bytes() for trace in self.__network_traffic]
        if 'resp_pkts' in attributes_value_dict:
            attributes_value_dict['resp_pkts'] = [trace.get_list_of_resp_pkts() for trace in self.__network_traffic]
        if 'resp_ip_bytes' in attributes_value_dict:
            attributes_value_dict['resp_ip_bytes'] = [trace.get_list_of_resp_ip_bytes() for trace in self.__network_traffic]

        return attributes_value_dict


    def discretize_attributes_equal_width(self, n_bins_dict: dict) -> None:
        """Discretizes all the attribute with equal width discretization

        Possible values of the attributes_to_discretize:
            #. orig_bytes
            #. resp_bytes
            #. missed_bytes
            #. orig_pkts
            #. duration
            #. orig_ip_bytes
            #. resp_pkts
            #. resp_ip_bytes

        :param n_bins_dict: dictionary where the key is the attribute to witch apply discretization and the value is the number of bins for that attribute
        :type n_bins_dict: dict
        """        
        attributes_to_discretize = list(n_bins_dict.keys())
        
        if 'orig_bytes' in attributes_to_discretize:
            Event.disc_orig_bytes = Equal_Width_Discretizer(n_bins_dict['orig_bytes'])
        if 'resp_bytes' in attributes_to_discretize:
            Event.disc_resp_bytes = Equal_Width_Discretizer(n_bins_dict['resp_bytes'])
        if 'missed_bytes' in attributes_to_discretize:
            Event.disc_missed_bytes = Equal_Width_Discretizer(n_bins_dict['missed_bytes'])
        if 'orig_pkts' in attributes_to_discretize:
            Event.disc_orig_pkts = Equal_Width_Discretizer(n_bins_dict['orig_pkts'])
        if 'duration' in attributes_to_discretize:
            Event.disc_duration = Equal_Width_Discretizer(n_bins_dict['duration'])
        if 'orig_ip_bytes' in attributes_to_discretize:
            Event.disc_orig_ip_bytes = Equal_Width_Discretizer(n_bins_dict['orig_ip_bytes'])
        if 'resp_pkts' in attributes_to_discretize:
            Event.disc_resp_pkts = Equal_Width_Discretizer(n_bins_dict['resp_pkts'])
        if 'resp_ip_bytes' in attributes_to_discretize: 
            Event.disc_resp_ip_bytes = Equal_Width_Discretizer(n_bins_dict['resp_ip_bytes'])
        
        self.__apply_discretization(attributes_to_discretize)

    def discretize_attributes_equal_height(self, n_bins_dict: dict) -> None:
        """Discretizes all the attribute with equal height discretization

        Possible values of the attributes_to_discretize:
            #. orig_bytes
            #. resp_bytes
            #. missed_bytes
            #. orig_pkts
            #. duration
            #. orig_ip_bytes
            #. resp_pkts
            #. resp_ip_bytes

        :param n_bins_dict: dictionary where the key is the attribute to witch apply discretization and the value is the number of bins for that attribute
        :type n_bins_dict: dict
        """
        attributes_to_discretize = set(n_bins_dict.keys())
        
        if 'orig_bytes' in attributes_to_discretize:
            Event.disc_orig_bytes = Equal_Height_Discretizer(n_bins_dict['orig_bytes'])
        if 'resp_bytes' in attributes_to_discretize:
            Event.disc_resp_bytes = Equal_Height_Discretizer(n_bins_dict['resp_bytes'])
        if 'missed_bytes' in attributes_to_discretize:
            Event.disc_missed_bytes = Equal_Height_Discretizer(n_bins_dict['missed_bytes'])
        if 'orig_pkts' in attributes_to_discretize:
            Event.disc_orig_pkts = Equal_Height_Discretizer(n_bins_dict['orig_pkts'])
        if 'duration' in attributes_to_discretize:
            Event.disc_duration = Equal_Height_Discretizer(n_bins_dict['duration'])
        if 'orig_ip_bytes' in attributes_to_discretize:
            Event.disc_orig_ip_bytes = Equal_Height_Discretizer(n_bins_dict['orig_ip_bytes'])
        if 'resp_pkts' in attributes_to_discretize:
            Event.disc_resp_pkts = Equal_Height_Discretizer(n_bins_dict['resp_pkts'])
        if 'resp_ip_bytes' in attributes_to_discretize: 
            Event.disc_resp_ip_bytes = Equal_Height_Discretizer(n_bins_dict['resp_ip_bytes'])

        self.__apply_discretization(attributes_to_discretize)

    def __apply_discretization(self, attributes_to_discretize: set):
        """Creates bins for every attribute

        Possible values of the attributes_to_discretize:
            #. orig_bytes
            #. resp_bytes
            #. missed_bytes
            #. orig_pkts
            #. duration
            #. orig_ip_bytes
            #. resp_pkts
            #. resp_ip_bytes

        :param attributes_to_discretize: set of all the attribute for which to create the bins
        :type attributes_to_discretize: set
        """
        attributes_value_dict = self.__get_list_of_all_attributes(attributes_to_discretize)

        if 'orig_bytes' in attributes_to_discretize:
            Event.disc_orig_bytes.discretize(attributes_value_dict['orig_bytes'])
        if 'resp_bytes' in attributes_to_discretize:
            Event.disc_resp_bytes.discretize(attributes_value_dict['resp_bytes'])
        if 'missed_bytes' in attributes_to_discretize:
            Event.disc_missed_bytes.discretize(attributes_value_dict['missed_bytes'])
        if 'orig_pkts' in attributes_to_discretize:
            Event.disc_orig_pkts.discretize(attributes_value_dict['orig_pkts'])
        if 'duration' in attributes_to_discretize:
            Event.disc_duration.discretize(attributes_value_dict['duration'])
        if 'orig_ip_bytes' in attributes_to_discretize:
            Event.disc_orig_ip_bytes.discretize(attributes_value_dict['orig_ip_bytes'])
        if 'resp_pkts' in attributes_to_discretize:
            Event.disc_resp_pkts.discretize(attributes_value_dict['resp_pkts'])
        if 'resp_ip_bytes' in attributes_to_discretize: 
            Event.disc_resp_ip_bytes.discretize(attributes_value_dict['resp_ip_bytes'])
            
