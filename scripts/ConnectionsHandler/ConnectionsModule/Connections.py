import json
from dataclasses import dataclass

class RowHistory:
    '''
    Class that manages the history of a single row, takes the string history
    and according to its characters sets single fields of this object to their value

    :param history: history to be converted
    :type history: str
    :param orig_syn: Origin sent this number of packets with a SYN bit set w/o the ACK bit set
    :type orig_syn: int
    :param orig_fin: Origin sent this number of packets with a FIN bit set
    :type orig_fin: int
    :param orig_syn_ack: Origin sent this number of packets with a SYN with the ACK bit set
    :type orig_syn_ack: int
    :param orig_rest: Origin sent this number of packets with a RST bit set
    :type orig_rest: int
    :param resp_syn: Responder sent this number of packets with a SYN bit set w/o the ACK bit set
    :type resp_syn: int
    :param resp_fin: Responder sent this number of packets with a FIN bit set 
    :type resp_fin: int
    :param resp_syn_ack: Responder sent this number of packets with a SYN with the ACK bit set
    :type resp_syn_ack: int
    :param resp_rest: Responder sent this number of packets with a RST bit set
    :type resp_rest: int
    :param orig_ack: Origin sent a packet with ACK bit set
    :type orig_ack: bool
    :param orig_payload: Origin sent a payload
    :type orig_payload: bool
    :param orig_inconsistent: Origin packet was inconsistent (e.g. FIN+RST bits set)
    :type orig_inconsistent: bool
    :param orig_multi_flag: Origin sent a multi-flag packet (SYN+FIN or SYN+RST bits set)
    :type orig_multi_flag: bool
    :param resp_ack: Responder sent a packet with ACK bit set
    :type resp_ack: bool
    :param resp_payload: Responder sent a payload
    :type resp_payload: bool
    :param resp_inconsistent: Responder packet was inconsistent (e.g. FIN+RST bits set)
    :type resp_inconsistent: bool
    :param resp_multi_flag: Responder sent a multi-flag packet (SYN+FIN or SYN+RST bits set)
    :type resp_multi_flag: bool
    :param orig_bad_checksum: Origin sent this number of packets with a bad checksum
    :type orig_bad_checksum: int 
    :param orig_content_gap: Origin sent this number of packets with content gap
    :type orig_content_gap: int 
    :param orig_retransmitted_payload: Origin retransmitted this number of packets with payload
    :type orig_retransmitted_payload: int 
    :param orig_zero_window: Origin sent this number of packet with zero window
    :type orig_zero_window: int 
    :param resp_bad_checksum: Responder sent this number of packets with a bad checksum
    :type resp_bad_checksum: int 
    :param resp_content_gap: Responder sent this number of packets with content gap
    :type resp_content_gap: int 
    :param resp_retransmitted_payload: Responder retransmitted this number of packets with payload
    :type resp_retransmitted_payload: int 
    :param resp_zero_window: Responder sent this number of packet with zero window
    :type resp_zero_window: int 
    :param conn_dir_flipped: Connection direction was flipped by Zeek's heuristic
    :type conn_dir_flipped: bool
    '''

    def __init__(self, history: str=None) -> None:
        """The constructor initialize the parameters required and if history is given,
        it analyze the string and assigns the relativa values to the fields

        :param history: string to be analyzed, defaults to None
        :type history: str, optional
        """        
        self.__history = history if history is not None else ''

        # S, F, H, R
        self.__orig_syn                   = 0
        self.__orig_fin                   = 0
        self.__orig_syn_ack               = 0
        self.__orig_rest                  = 0

        # s, f, h, r
        self.__resp_syn                   = 0
        self.__resp_fin                   = 0
        self.__resp_syn_ack               = 0
        self.__resp_rest                  = 0
        
        # A, D, I, Q
        self.__orig_ack                   = False
        self.__orig_payload               = False
        self.__orig_inconsistent          = False
        self.__orig_multi_flag            = False

        # a, d, i, q
        self.__resp_ack                   = False
        self.__resp_payload               = False
        self.__resp_inconsistent          = False
        self.__resp_multi_flag            = False
        
        # C, G, T, W
        self.__orig_bad_checksum          = 0
        self.__orig_content_gap           = 0
        self.__orig_retransmitted_payload = 0
        self.__orig_zero_window           = 0

        # c, g, t, w
        self.__resp_bad_checksum          = 0
        self.__resp_content_gap           = 0
        self.__resp_retransmitted_payload = 0
        self.__resp_zero_window           = 0

        # ^
        self.__conn_dir_flipped           = False
        
        self.analyze_history()

    def analyze_history(self, history: str=None) -> None:
        """Based on the field history, this analyze the history string and changes
        all the fields of this object. If given a history, this will be analyzed and set
        as this object history

        :param history: the history to be analyzed, defaults to None
        :type history: str, optional
        """

        if history is not None:
            self.__history = history

        for c in self.__history:
            if c == 'S': self.__orig_syn += 1
            elif c == 'F': self.__orig_fin += 1
            elif c == 'H': self.__orig_syn_ack += 1
            elif c == 'R': self.__orig_rest += 1
            
            elif c == 's': self.__resp_syn += 1
            elif c == 'f': self.__resp_fin += 1
            elif c == 'h': self.__resp_syn_ack += 1
            elif c == 'r': self.__resp_rest += 1

            elif c == 'A': self.__orig_ack = True
            elif c == 'D': self.__orig_payload = True
            elif c == 'I': self.__orig_inconsistent = True
            elif c == 'Q': self.__orig_multi_flag = True

            elif c == 'a': self.__resp_ack = True
            elif c == 'd': self.__resp_payload = True
            elif c == 'i': self.__resp_inconsistent = True
            elif c == 'q': self.__resp_multi_flag = True

            elif c == 'C': self.__orig_bad_checksum += 1
            elif c == 'G': self.__orig_content_gap += 1
            elif c == 'T': self.__orig_retransmitted_payload += 1
            elif c == 'W': self.__orig_zero_window += 1

            elif c == 'c': self.__resp_bad_checksum += 1
            elif c == 'g': self.__resp_content_gap += 1
            elif c == 't': self.__resp_retransmitted_payload += 1
            elif c == 'w': self.__resp_zero_window += 1

            elif c == '^': self.__conn_dir_flipped = True

    def get_history_with_values(self, history: str=None) -> list:
        """Returns a list of the tuples where the first element of the tuple
        is the character red, the second is the value itself.__ If a history string is given, 
        the list is relative to that history and this object's history value is changed

        :param history: history to be transformed, defaults to None
        :type history: str, optional
        :return: list of the tuples of the history
        :rtype: list
        """        

        if history is not None:
            self.analyze_history(history)
        
        return [self.__history,
            ('S', self.__orig_syn),
            ('F', self.__orig_fin),
            ('H', self.__orig_syn_ack),
            ('R', self.__orig_rest),

            ('s', self.__resp_syn),
            ('f', self.__resp_fin),
            ('h', self.__resp_syn_ack),
            ('r', self.__resp_rest),

            ('A', self.__orig_ack),
            ('D', self.__orig_payload),
            ('I', self.__orig_inconsistent),
            ('Q', self.__orig_multi_flag),

            ('a', self.__resp_ack),
            ('d', self.__resp_payload),
            ('i', self.__resp_inconsistent),
            ('q', self.__resp_multi_flag),

            ('C', self.__orig_bad_checksum),
            ('G', self.__orig_content_gap),
            ('T', self.__orig_retransmitted_payload),
            ('W', self.__orig_zero_window),

            ('c', self.__resp_bad_checksum),
            ('g', self.__resp_content_gap),
            ('t', self.__resp_retransmitted_payload),
            ('w', self.__resp_zero_window),

            ('^', self.__conn_dir_flipped),
        ]

    def get_history_with_description(self, history: str=None) -> list:
        """Returns a list where for each element, there is a string describing the letter red
        at that position. If a history string is given, the list is relative to that history and
        this object's history value is changed

        :param history: history to be transformed, defaults to None
        :type history: str, optional
        :return: list of the description of each letter
        :rtype: list
        """        
        """Returns a list where for each element, there is a string describing the letter red
        at that position

        :return: list of the description of each letter
        :rtype: list
        """
        if history is not None:
            self.analyze_history(history)

        out_list = [] # lista delle stringhe corrispondenti alle fasi della history
        for i, c in enumerate(self.__history):
            if c == 'S': out_list.append(f'{i + 1}. Origin sent a packet with a SYN bit set w/o the ACK bit set')
            elif c == 'F': out_list.append(f'{i + 1}. Origin sent a packet with a FIN bit set')
            elif c == 'H': out_list.append(f'{i + 1}. Origin sent a packet with a SYN with the ACK bit set')
            elif c == 'R': out_list.append(f'{i + 1}. Origin sent a packet with a RST bit set')
            
            elif c == 's': out_list.append(f'{i + 1}. Responder sent a packet with a SYN bit set w/o the ACK bit set')
            elif c == 'f': out_list.append(f'{i + 1}. Responder sent a packet with a FIN bit set ')
            elif c == 'h': out_list.append(f'{i + 1}. Responder sent a packet with a SYN with the ACK bit set')
            elif c == 'r': out_list.append(f'{i + 1}. Responder sent a packet with a RST bit set')

            elif c == 'A': out_list.append(f'{i + 1}. Origin sent a packet with ACK bit set')
            elif c == 'D': out_list.append(f'{i + 1}. Origin sent a payload')
            elif c == 'I': out_list.append(f'{i + 1}. Origin packet was inconsistent (e.g. FIN+RST bits set)')
            elif c == 'Q': out_list.append(f'{i + 1}. Origin sent a multi-flag packet (SYN+FIN or SYN+RST bits set)')

            elif c == 'a': out_list.append(f'{i + 1}. Responder sent a packet with ACK bit set')
            elif c == 'd': out_list.append(f'{i + 1}. Responder sent a payload')
            elif c == 'i': out_list.append(f'{i + 1}. Responder packet was inconsistent (e.g. FIN+RST bits set)')
            elif c == 'q': out_list.append(f'{i + 1}. Responder sent a multi-flag packet (SYN+FIN or SYN+RST bits set)')

            elif c == 'C': out_list.append(f'{i + 1}. Origin sent a packet with a bad checksum')
            elif c == 'G': out_list.append(f'{i + 1}. Origin sent a packet with content gap')
            elif c == 'T': out_list.append(f'{i + 1}. Origin retransmitted a packet with payload')
            elif c == 'W': out_list.append(f'{i + 1}. Origin sent a packet with zero window')

            elif c == 'c': out_list.append(f'{i + 1}. Responder sent a packet with a bad checksum')
            elif c == 'g': out_list.append(f'{i + 1}. Responder sent a packet with content gap')
            elif c == 't': out_list.append(f'{i + 1}. Responder retransmitted a packet with payload')
            elif c == 'w': out_list.append(f'{i + 1}. Responder sent a packet with zero window')

            elif c == '^': out_list.append(f"{i + 1}. Connection direction was flipped by Zeek's heuristic")

        return out_list

    def to_json_obj(self) -> object:
        """
        converts this class object to an object that can be easily dumped in a json file

        :return: object that can be converted to a json file
        :rtype: object
        """
        return {
            'history': self.__history,
            'S': self.__orig_syn,
            'F': self.__orig_fin,
            'H': self.__orig_syn_ack,
            'R': self.__orig_rest,
            's': self.__resp_syn,
            'f': self.__resp_fin,
            'h': self.__resp_syn_ack,
            'r': self.__resp_rest,
            'A': self.__orig_ack,
            'D': self.__orig_payload,
            'I': self.__orig_inconsistent,
            'Q': self.__orig_multi_flag,
            'a': self.__resp_ack,
            'd': self.__resp_payload,
            'i': self.__resp_inconsistent,
            'q': self.__resp_multi_flag,
            'C': self.__orig_bad_checksum,
            'G': self.__orig_content_gap,
            'T': self.__orig_retransmitted_payload,
            'W': self.__orig_zero_window,
            'c': self.__resp_bad_checksum,
            'g': self.__resp_content_gap,
            't': self.__resp_retransmitted_payload,
            'w': self.__resp_zero_window,
            '^': self.__conn_dir_flipped,
        }


@dataclass(frozen=True)
class Connection:
    '''
    Class of a single connection registered

    This class contains all of the data that are going to be used
    to classify this connection

    :param uid: unique id of this connection
    :type uid: str
    :param ts: timestamp of this connection
    :type ts: str
    :param service: An identification of an application protocol being sent over the connection.
    :type service: str
    :param state: state of the connection
    :type state: str
    :param duration: How long the connection lasted. For 3-way or 4-way connection tear-downs, this will not include the final ACK.
    :type duration: float
    :param orig_bytes: number of bytes sent by the origin
    :type orig_bytes: int
    :param resp_bytes: number of bytes sent by the responder
    :type resp_bytes: int
    :param conn_state: state of this connection
    :type conn_state: str
    :param missed_bytes: bytes missed during this connection
    :type missed_bytes: int
    :param history: state history of this connection.
    :type history: RowHistory
    :param orig_pkts: Number of packets that the originator sent
    :type orig_pkts: int
    :param orig_ip_bytes: Number of IP level bytes that the originator sent (as seen on the wire, taken from the IP total_length header field
    :type orig_ip_bytes: int
    :param resp_pkts: Number of packets that the responder sent.
    :type resp_pkts: int
    :param resp_ip_bytes: Number of IP level bytes that the responder sent (as seen on the wire, taken from the IP total_length header field
    :type resp_ip_bytes: int
    '''
    uid: str
    ts: str
    services: str
    duration: float
    orig_bytes: int
    resp_bytes: int
    conn_state: str
    missed_bytes: int
    history: RowHistory
    orig_pkts: int
    orig_ip_bytes: int
    resp_pkts: int
    resp_ip_bytes: int

    def to_json_obj(self) -> object:
        """
        converts this class object to an object that can be easily dumped in a json file

        :return: object that can be converted to a json file
        :rtype: object
        """
        return {
            'uid': self.uid,
            'ts': self.ts,
            'services': self.services,
            'duration': self.duration,
            'orig_bytes': self.orig_bytes,
            'resp_bytes': self.resp_bytes,
            'conn_state': self.conn_state,
            'missed_bytes': self.missed_bytes,
            'history': self.history,
            'orig_pkts': self.orig_pkts,
            'orig_ip_bytes': self.orig_ip_bytes,
            'resp_pkts': self.resp_pkts,
            'resp_ip_bytes': self.resp_ip_bytes,
        }

    ## method generated by dataclass
    # delattr
    # eq
    # hash
    # init
    # repr
    # setattr


class NetworkConversation:
    """
    This class contains all the connections that are being originated by the same
    ip and port of origin and responder hosts.

    :param orig_ip: ip of the host that started this conversation
    :type orig_ip:  str
    :param orig_port: port of the host that started this conversation
    :type orig_port: str
    :param resp_ip: ip of the host that has been requested to start this conversation
    :type resp_ip: str
    :param resp_port: port of the host that has been requested to start this conversation
    :type resp_port: str
    :param ts_on_open: timestamp of the first packet of the connection that started this conversation
    :type ts_on_open: str
    :param proto: protocol used for this conversation
    :type proto: str
    :param connections: set of the connection between this 2 hosts with these ports
    :type connections: set[Connection]
    """

    def __init__(self, orig_ip: str, orig_port: int, resp_ip: str, resp_port: int, ts_on_open: str, proto: str):
        self.orig_ip = orig_ip
        self.orig_port = orig_port
        self.resp_ip = resp_ip
        self.resp_port = resp_port
        self.ts_on_open = ts_on_open
        self.proto = proto
        self.connections = set()

    def add_packet(self, p: Connection, elapsed_ts: float=None) -> None:
        """
        Class that contains multiple Connections with the same id

        :param p: the connection to be added to this wrapper
        :type p: Connection
        :param elapsed_ts: max window time so that a connection can be considered to belong to this NetworkConversation
        :type elapsed_ts: float
        :raises KeyError: raises a KeyError if the id of the connection doesn't match
        """
        if elapsed_ts is None:
            if p.generate_id() == self.id:
                self.connections.append(p)
            else:
                raise KeyError
        else:
            pass # TODO
    
    def to_json_obj(self) -> object:
        """Convert this object to an object that can be easily converted to a json

        :return: this object as a dumpable object
        :rtype: object
        """
        connections = []
        for connection in self.connections:
            connections.append(connection.to_json_obj())

        return {
            'orig_ip': self.orig_ip,
            'orig_port': self.orig_port,
            'resp_ip': self.resp_ip,
            'resp_port': self.resp_port,
            'ts_on_open': self.ts_on_open,
            'proto': self.proto,
            'connections': connections,
        }
        
    def generate_id(self) -> str:
        """
        generate the id for this conversation based on origin ip, origin port, responder ip, responder port, timestamp

        :return: the id based on the origin and responder ip and port
        :rtype: str
        """        
        return self.orig_ip + " " + self.orig_port + " " + self.resp_ip + " " + self.resp_port + " " + self.ts_on_open


class NetworkTrafficController:
    """
    Class that contains the method used to filter and organize packets

    :param path_of_file_input: path of the file that contains the logs to be acquired
    :type path_of_file_input: str, optional
    :param path_of_file_output: path of the file where the preprocessed lines are stored or will be stored
    :type path_of_file_output: str, optional
    :param path_of_file_json: path of the file where to write the json file
    :type path_of_file_json: str, optional
    :param lines_to_remove_ash: set of the # to remove from the file
    :type lines_to_remove_ash: set[str], optional
    :param strings_to_filter_rows: set of string to be filtered out
    :type strings_to_filter_rows: set[str], optional
    :param network_traffic: set of the NetworkConversation
    :type network_traffic: set[NetworkConversation]
    :param networkConversation_pos_dict: dict that contains the indices of network_traffic
    :type networkConversation_pos_dict: dict{str: int}
    """
    def __init__(self, 
        path_of_file_input: str='',
        path_of_file_output: str='',
        path_of_file_json: str='',
        lines_to_remove_ash: set=[],
        strings_to_filter_rows: set=[]) -> None:
        """Constructor Method
        """
        self.path_of_file_input = path_of_file_input
        self.path_of_file_output = path_of_file_output
        self.path_of_file_json = path_of_file_json
        self.lines_to_remove_ash = lines_to_remove_ash
        self.strings_to_filter_rows = strings_to_filter_rows
        self.network_traffic = []
        self.networkConversation_pos_dict = {}
    
    def load_paths_and_filters_from_config_file(self, config_file_path):
        """
        loads all path and filters form the ini file

        :param config_file_path: path of the configuration path
        :type config_file_path: str
        """   
        import configparser
        print('reading config option from file...')
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # checks if Files is in config.ini file
        if 'Files' in config:
            self.path_of_file_input = config['Files']['path_of_file_input'] if 'path_of_file_input' in config['Files'] else ''
            self.path_of_file_output = config['Files']['path_of_file_output'] if 'path_of_file_output' in config['Files'] else ''
            self.path_of_file_json = config['Files']['path_of_file_json']  if 'path_of_file_json' in config['Files'] else ''
        else:
            self.path_of_file_input = self.path_of_file_input if self.path_of_file_input != '' else ''
            self.path_of_file_output = self.path_of_file_output if self.path_of_file_output != '' else ''
            self.path_of_file_json = self.path_of_file_json if self.path_of_file_json != '' else ''

        # checks if Filters is in config.ini file
        if 'Filters' in config:
            self.lines_to_remove_ash = config['Filters']['lines_to_remove_ash']  if 'lines_to_remove_ash' in config['Filters'] else ''
            self.strings_to_filter_rows = config['Filters']['strings_to_filter_rows']  if 'strings_to_filter_rows' in config['Filters'] else ''

            self.lines_to_remove_ash = self.lines_to_remove_ash.replace('\'', '').split(',')
            self.strings_to_filter_rows = self.strings_to_filter_rows.replace('\'', '').split(',')
        else:
            self.lines_to_remove_ash = '' 
            self.strings_to_filter_rows = '' 

        print('...reading complete')


    def open_stored_preprocessed_lines(self) -> list:
        """
        read stored preprocessed lines from a file specified in the
        path_of_file_output of this object

        :return: pre-processed lines red from file
        :rtype: list(str)
        """
        print('reading stored lines from file...')
        with open(self.path_of_file_output, 'r') as f:
            self.preprocessed_lines = []
            for line in f:
                self.preprocessed_lines.append(line)

            print('...reading complete')
        return self.preprocessed_lines

    def print_preprocessed_lines_to_file(self):
        """
        prints preprocessed lines to a file specified in the path_of_file_output
        field of this object

        """
        print('printing preprocessed lines to file...')
        with open(self.path_of_file_output, 'w') as f_out:
            # writing lines to new file
            for line in self.preprocessed_lines:
                f_out.write(line)
        print('...printing complete')

    def normalize_lines(self) -> list:
        """
        normalize lines from file and if the path_of_file_output
        is set, prints the lines to a file

        :return: lines that have been normalized
        :rtype: list(str)
        """
        print('normalizing lines...')
        self.preprocessed_lines = []
        # normalizing lines
        with open(self.path_of_file_input, "r+") as f_in:
            for line in f_in:
                # removing comment lines
                to_remove = False
                for line_to_check in self.lines_to_remove:
                    if line.startswith(line_to_check):
                        to_remove = True
                if not(to_remove):
                    # replacing comment in field/types lines
                    for line_to_check in self.lines_to_remove_ash:
                        if line.startswith(line_to_check):
                            line = line.replace(line_to_check, '')
                            break

                    # removing unnecessary strings
                    for string in self.strings_to_filter_rows: 
                        line = line.replace(string, '')
                    self.preprocessed_lines.append(line)
        print('...normalization completed')
        return self.preprocessed_lines

    def conv_lines_to_NetworkConversation_set(self) -> set:
        """
        Convert a list of preprocessed lines to a list of Connection and inserts them into the 
        NetworkConversation set

        :return: set of strings that have been normalized
        :rtype: set(str)
        """        
        print('converting preprocessed lines to list of packet wrappers...')
        packets = self.__conv_lines_to_list_of_Connection()
        
        connections_dict = {}
        for p in packets:
            id = p.generate_id()

            if id not in connections_dict:
                connections_dict[id] = Connection()
            else:
                connections_dict[id].add_packet(p)
        print('...conversion completed')
        self.connections_list = list(connections_dict.values())
        return self.connections_list
        
    def __conv_lines_to_list_of_Connection(self) -> list:
        """
        converts a list of preprocessed lines to a list of Connections

        :return: list of Connections converted from list of lines
        :rtype: list(Connection)
        """        
        packets = []
        
        for line in self.preprocessed_lines:
            packets.append(self.__conv_conn_line_to_Connection(line))

        return packets

    def __conv_conn_line_to_Connection(self, line: str) -> Connection:
        """
        converts a conn.log line to a Connection

        :param line: line to be converted to Connection
        :type line: str
        :return: Connection converted from line
        :rtype: Connection
        """
        list_to_pack = line.split('\t')

        # getting info to insert in Connection
        uid = list_to_pack[1]
        orig_ip = list_to_pack[2]
        orig_port = list_to_pack[3]
        resp_ip = list_to_pack[4]
        resp_port = list_to_pack[5]
        ts = list_to_pack[0]
        services = list_to_pack[7]
        state = list_to_pack[11]

        return Connection(uid, orig_ip, orig_port, resp_ip, resp_port, ts, services, state)
        
    def print_NetworkConversation_list_to_json_file(self):
        """prints all the Network Conversations list to a json file
        """
        print('writing the list of Connections to a json file...')
        with open(self.path_of_file_json, 'w') as f:
            to_json = []
            for pw in self.connections_list:
                to_json.append(pw.to_json_obj())
            
            json.dump(to_json, f, indent=4)
        print('...writing completed')




