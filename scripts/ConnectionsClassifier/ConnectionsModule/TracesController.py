from ConnectionsModule.EventHistory import EventHistory
from .Trace import Trace
from .Event import Event
from DiscretizerModule.Equal_Frequency_Discretizer import Equal_Frequency_Discretizer
from DiscretizerModule.Equal_Width_Discretizer import Equal_Width_Discretizer
from DiscretizerModule.DISCRETIZATION_TYPE import DISCRETIZATION_TYPE

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

    def __get_list_of_attribute(self, attribute: str) -> list:
        """Returns a list of the values of the attribute specified in attribute

        Possible values of attribute_to_discretize:
            - orig_bytes
            - resp_bytes
            - missed_bytes
            - orig_pkts
            - duration
            - orig_ip_bytes
            - resp_pkts
            - resp_ip_bytes

        :param attribute: name of the attribute from where to collect data from
        :type attribute: str
        :return: list of all the values of that attribute
        :rtype: list
        :raises ValueError: raised if attribute is not one of the attributes to discretize
        """
        from itertools import chain

        if 'orig_bytes' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_bytes() for trace in self.__network_traffic]))
        elif 'resp_bytes' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_bytes() for trace in self.__network_traffic]))
        elif 'missed_bytes' == attribute:
            return list(chain.from_iterable([trace.get_list_of_missed_bytes() for trace in self.__network_traffic]))
        elif 'orig_pkts' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_pkts() for trace in self.__network_traffic]))
        elif 'duration' == attribute:
            return list(chain.from_iterable([trace.get_list_of_duration() for trace in self.__network_traffic]))
        elif 'orig_ip_bytes' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_ip_bytes() for trace in self.__network_traffic]))
        elif 'resp_pkts' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_pkts() for trace in self.__network_traffic]))
        elif 'resp_ip_bytes' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_ip_bytes() for trace in self.__network_traffic]))

        elif 'orig_syn' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_syn() for trace in self.__network_traffic]))
        elif 'orig_fin' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_fin() for trace in self.__network_traffic]))
        elif 'orig_syn_ack' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_syn_ack() for trace in self.__network_traffic]))
        elif 'orig_rst' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_rst() for trace in self.__network_traffic]))
        elif 'resp_syn' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_syn() for trace in self.__network_traffic]))
        elif 'resp_fin' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_fin() for trace in self.__network_traffic]))
        elif 'resp_syn_ack' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_syn_ack() for trace in self.__network_traffic]))
        elif 'resp_rst' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_rst() for trace in self.__network_traffic]))
        elif 'orig_bad_checksum' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_bad_checksum() for trace in self.__network_traffic]))
        elif 'orig_content_gap' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_content_gap() for trace in self.__network_traffic]))
        elif 'orig_retransmitted_payload' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_retransmitted_payload() for trace in self.__network_traffic]))
        elif 'orig_zero_window' == attribute:
            return list(chain.from_iterable([trace.get_list_of_orig_zero_window() for trace in self.__network_traffic]))
        elif 'resp_bad_checksum' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_bad_checksum() for trace in self.__network_traffic]))
        elif 'resp_content_gap' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_content_gap() for trace in self.__network_traffic]))
        elif 'resp_retransmitted_payload' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_retransmitted_payload() for trace in self.__network_traffic]))
        elif 'resp_zero_window' == attribute:
            return list(chain.from_iterable([trace.get_list_of_resp_zero_window() for trace in self.__network_traffic]))
        else:
            raise ValueError('attribute must be one of these: orig_bytes, resp_bytes, missed_bytes, orig_pkts, duration, orig_ip_bytes, resp_pkts, resp_ip_bytes')

    def discretize_attributes(self, disc_type: DISCRETIZATION_TYPE, n_bins_dict: dict) -> None:
        """Discretizes all the attribute with equal width of frequency discretization depending of the type given in disc_type

        Possible values of the attributes_to_discretize:
            #. orig_bytes
            #. resp_bytes
            #. missed_bytes
            #. orig_pkts
            #. duration
            #. orig_ip_bytes
            #. resp_pkts
            #. resp_ip_bytes

        :param disc_type: the type of discretization to instantiate
        :type disc_type: DISCRETIZATION_TYPE
        :param n_bins_dict: dictionary where the key is the attribute to witch apply discretization and the value is the number of bins for that attribute
        :type n_bins_dict: dict
        :raises ValueError: raised if the disc_type is not either EQUAL_WIDTH or EQUAL_FREQUENCY
        """
        attributes_to_discretize = list(n_bins_dict.keys())
        
        if disc_type == DISCRETIZATION_TYPE.EQUAL_WIDTH:
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
                
            if 'orig_syn' in attributes_to_discretize: 
                EventHistory.disc_orig_syn = Equal_Width_Discretizer(n_bins_dict['orig_syn'])
            if 'orig_fin' in attributes_to_discretize: 
                EventHistory.disc_orig_fin = Equal_Width_Discretizer(n_bins_dict['orig_fin'])
            if 'orig_syn_ack' in attributes_to_discretize: 
                EventHistory.disc_orig_syn_ack = Equal_Width_Discretizer(n_bins_dict['orig_syn_ack'])
            if 'orig_rst' in attributes_to_discretize: 
                EventHistory.disc_orig_rst = Equal_Width_Discretizer(n_bins_dict['orig_rst'])
            if 'resp_syn' in attributes_to_discretize: 
                EventHistory.disc_resp_syn = Equal_Width_Discretizer(n_bins_dict['resp_syn'])
            if 'resp_fin' in attributes_to_discretize: 
                EventHistory.disc_resp_fin = Equal_Width_Discretizer(n_bins_dict['resp_fin'])
            if 'resp_syn_ack' in attributes_to_discretize: 
                EventHistory.disc_resp_syn_ack = Equal_Width_Discretizer(n_bins_dict['resp_syn_ack'])
            if 'resp_rst' in attributes_to_discretize: 
                EventHistory.disc_resp_rst = Equal_Width_Discretizer(n_bins_dict['resp_rst'])
            if 'orig_bad_checksum' in attributes_to_discretize: 
                EventHistory.disc_orig_bad_checksum = Equal_Width_Discretizer(n_bins_dict['orig_bad_checksum'])
            if 'orig_content_gap' in attributes_to_discretize: 
                EventHistory.disc_orig_content_gap = Equal_Width_Discretizer(n_bins_dict['orig_content_gap'])
            if 'orig_retransmitted_payload' in attributes_to_discretize: 
                EventHistory.disc_orig_retransmitted_payload = Equal_Width_Discretizer(n_bins_dict['orig_retransmitted_payload'])
            if 'orig_zero_window' in attributes_to_discretize: 
                EventHistory.disc_orig_zero_window = Equal_Width_Discretizer(n_bins_dict['orig_zero_window'])
            if 'resp_bad_checksum' in attributes_to_discretize: 
                EventHistory.disc_resp_bad_checksum = Equal_Width_Discretizer(n_bins_dict['resp_bad_checksum'])
            if 'resp_content_gap' in attributes_to_discretize: 
                EventHistory.disc_resp_content_gap = Equal_Width_Discretizer(n_bins_dict['resp_content_gap'])
            if 'resp_retransmitted_payload' in attributes_to_discretize: 
                EventHistory.disc_resp_retransmitted_payload = Equal_Width_Discretizer(n_bins_dict['resp_retransmitted_payload'])
            if 'resp_zero_window' in attributes_to_discretize: 
                EventHistory.disc_resp_zero_window = Equal_Width_Discretizer(n_bins_dict['resp_zero_window'])


        elif disc_type == DISCRETIZATION_TYPE.EQUAL_FREQUENCY:
            if 'orig_bytes' in attributes_to_discretize:
                Event.disc_orig_bytes = Equal_Frequency_Discretizer(n_bins_dict['orig_bytes'])
            if 'resp_bytes' in attributes_to_discretize:
                Event.disc_resp_bytes = Equal_Frequency_Discretizer(n_bins_dict['resp_bytes'])
            if 'missed_bytes' in attributes_to_discretize:
                Event.disc_missed_bytes = Equal_Frequency_Discretizer(n_bins_dict['missed_bytes'])
            if 'orig_pkts' in attributes_to_discretize:
                Event.disc_orig_pkts = Equal_Frequency_Discretizer(n_bins_dict['orig_pkts'])
            if 'duration' in attributes_to_discretize:
                Event.disc_duration = Equal_Frequency_Discretizer(n_bins_dict['duration'])
            if 'orig_ip_bytes' in attributes_to_discretize:
                Event.disc_orig_ip_bytes = Equal_Frequency_Discretizer(n_bins_dict['orig_ip_bytes'])
            if 'resp_pkts' in attributes_to_discretize:
                Event.disc_resp_pkts = Equal_Frequency_Discretizer(n_bins_dict['resp_pkts'])
            if 'resp_ip_bytes' in attributes_to_discretize: 
                Event.disc_resp_ip_bytes = Equal_Frequency_Discretizer(n_bins_dict['resp_ip_bytes'])

            if 'orig_syn' in attributes_to_discretize: 
                EventHistory.disc_orig_syn = Equal_Frequency_Discretizer(n_bins_dict['orig_syn'])
            if 'orig_fin' in attributes_to_discretize: 
                EventHistory.disc_orig_fin = Equal_Frequency_Discretizer(n_bins_dict['orig_fin'])
            if 'orig_syn_ack' in attributes_to_discretize: 
                EventHistory.disc_orig_syn_ack = Equal_Frequency_Discretizer(n_bins_dict['orig_syn_ack'])
            if 'orig_rst' in attributes_to_discretize: 
                EventHistory.disc_orig_rst = Equal_Frequency_Discretizer(n_bins_dict['orig_rst'])
            if 'resp_syn' in attributes_to_discretize: 
                EventHistory.disc_resp_syn = Equal_Frequency_Discretizer(n_bins_dict['resp_syn'])
            if 'resp_fin' in attributes_to_discretize: 
                EventHistory.disc_resp_fin = Equal_Frequency_Discretizer(n_bins_dict['resp_fin'])
            if 'resp_syn_ack' in attributes_to_discretize: 
                EventHistory.disc_resp_syn_ack = Equal_Frequency_Discretizer(n_bins_dict['resp_syn_ack'])
            if 'resp_rst' in attributes_to_discretize: 
                EventHistory.disc_resp_rst = Equal_Frequency_Discretizer(n_bins_dict['resp_rst'])
            if 'orig_bad_checksum' in attributes_to_discretize: 
                EventHistory.disc_orig_bad_checksum = Equal_Frequency_Discretizer(n_bins_dict['orig_bad_checksum'])
            if 'orig_content_gap' in attributes_to_discretize: 
                EventHistory.disc_orig_content_gap = Equal_Frequency_Discretizer(n_bins_dict['orig_content_gap'])
            if 'orig_retransmitted_payload' in attributes_to_discretize: 
                EventHistory.disc_orig_retransmitted_payload = Equal_Frequency_Discretizer(n_bins_dict['orig_retransmitted_payload'])
            if 'orig_zero_window' in attributes_to_discretize: 
                EventHistory.disc_orig_zero_window = Equal_Frequency_Discretizer(n_bins_dict['orig_zero_window'])
            if 'resp_bad_checksum' in attributes_to_discretize: 
                EventHistory.disc_resp_bad_checksum = Equal_Frequency_Discretizer(n_bins_dict['resp_bad_checksum'])
            if 'resp_content_gap' in attributes_to_discretize: 
                EventHistory.disc_resp_content_gap = Equal_Frequency_Discretizer(n_bins_dict['resp_content_gap'])
            if 'resp_retransmitted_payload' in attributes_to_discretize: 
                EventHistory.disc_resp_retransmitted_payload = Equal_Frequency_Discretizer(n_bins_dict['resp_retransmitted_payload'])
            if 'resp_zero_window' in attributes_to_discretize: 
                EventHistory.disc_resp_zero_window = Equal_Frequency_Discretizer(n_bins_dict['resp_zero_window'])
        else:
            raise ValueError('the type of discretization is not valid')
        
        for attribute in attributes_to_discretize:
            self.__apply_discretization(attribute)

    def __apply_discretization(self, attribute_to_discretize: str):
        """Creates bins for the attribute specified in attribute_to_discretize

        Possible values of the attributes_to_discretize:
            - orig_bytes
            - resp_bytes
            - missed_bytes
            - orig_pkts
            - duration
            - orig_ip_bytes
            - resp_pkts
            - resp_ip_bytes

        :param attribute_to_discretize: name of the attribute for which to create the bins
        :type attribute_to_discretize: str
        :raises ValueError: raised if attribute_to_discretize is not one of the attributes to discretize
        """
        attributes_values = self.__get_list_of_attribute(attribute_to_discretize)

        if 'orig_bytes' == attribute_to_discretize:
            Event.disc_orig_bytes.discretize(attributes_values)
        elif 'resp_bytes' == attribute_to_discretize:
            Event.disc_resp_bytes.discretize(attributes_values)
        elif 'missed_bytes' == attribute_to_discretize:
            Event.disc_missed_bytes.discretize(attributes_values)
        elif 'orig_pkts' == attribute_to_discretize:
            Event.disc_orig_pkts.discretize(attributes_values)
        elif 'duration' == attribute_to_discretize:
            Event.disc_duration.discretize(attributes_values)
        elif 'orig_ip_bytes' == attribute_to_discretize:
            Event.disc_orig_ip_bytes.discretize(attributes_values)
        elif 'resp_pkts' == attribute_to_discretize:
            Event.disc_resp_pkts.discretize(attributes_values)
        elif 'resp_ip_bytes' == attribute_to_discretize: 
            Event.disc_resp_ip_bytes.discretize(attributes_values)
        
        elif 'orig_syn' == attribute_to_discretize: 
            EventHistory.disc_orig_syn.discretize(attributes_values)
        elif 'orig_fin' == attribute_to_discretize: 
            EventHistory.disc_orig_fin.discretize(attributes_values)
        elif 'orig_syn_ack' == attribute_to_discretize: 
            EventHistory.disc_orig_syn_ack.discretize(attributes_values)
        elif 'orig_rst' == attribute_to_discretize: 
            EventHistory.disc_orig_rst.discretize(attributes_values)
        elif 'resp_syn' == attribute_to_discretize: 
            EventHistory.disc_resp_syn.discretize(attributes_values)
        elif 'resp_fin' == attribute_to_discretize: 
            EventHistory.disc_resp_fin.discretize(attributes_values)
        elif 'resp_syn_ack' == attribute_to_discretize: 
            EventHistory.disc_resp_syn_ack.discretize(attributes_values)
        elif 'resp_rst' == attribute_to_discretize: 
            EventHistory.disc_resp_rst.discretize(attributes_values)
        elif 'orig_bad_checksum' == attribute_to_discretize: 
            EventHistory.disc_orig_bad_checksum.discretize(attributes_values)
        elif 'orig_content_gap' == attribute_to_discretize: 
            EventHistory.disc_orig_content_gap.discretize(attributes_values)
        elif 'orig_retransmitted_payload' == attribute_to_discretize: 
            EventHistory.disc_orig_retransmitted_payload.discretize(attributes_values)
        elif 'orig_zero_window' == attribute_to_discretize: 
            EventHistory.disc_orig_zero_window.discretize(attributes_values)
        elif 'resp_bad_checksum' == attribute_to_discretize: 
            EventHistory.disc_resp_bad_checksum.discretize(attributes_values)
        elif 'resp_content_gap' == attribute_to_discretize: 
            EventHistory.disc_resp_content_gap.discretize(attributes_values)
        elif 'resp_retransmitted_payload' == attribute_to_discretize: 
            EventHistory.disc_resp_retransmitted_payload.discretize(attributes_values)
        elif 'resp_zero_window' == attribute_to_discretize: 
            EventHistory.disc_resp_zero_window.discretize(attributes_values)
        else:
            raise ValueError('attribute_to_discretize must be one of these: orig_bytes, resp_bytes, missed_bytes, orig_pkts, duration, orig_ip_bytes, resp_pkts, resp_ip_bytes') 
