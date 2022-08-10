import json
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Packet:
    '''
    Class of a single packet registered

    This class contains all of the data that are going to be used
    to classify this packet

    Args:
        uid (str): unique id of this connection
        orig_ip (str): ip of the origin host
        orig_port (int): port of the origin host
        resp_ip (str): ip of the responder host
        resp_port (int): port of the responder host
        ts (str): timestamp of this connection
        services (str): service used for this connection
        state (str): state of the connection
    '''
    uid: str
    orig_ip: str
    orig_port: int
    resp_ip: str
    resp_port: int
    ts: str
    services: str
    state: str

    def generate_id(self) -> str:
        """
        generate an id of this packet

        Returns:
            str: the id based on the origin and responder ip and port
        """        
        return self.orig_ip + " " + self.orig_port + " " + self.resp_ip + " " + self.resp_port

    def to_json_obj(self) -> object:
        """
        converts this class object to an object that can be easily dumped in a json file

        Returns:
            object: object that can be converted to a json file
        """        
        return {
            "uid": self.uid,
            "orig_ip": self.orig_ip,
            "orig_port": self.orig_port,
            "resp_ip": self.resp_ip,
            "resp_port": self.resp_port,
            "ts": self.ts,
            "services": self.services,
            "state": self.state,
        }

    ## method generated by dataclass
    # delattr
    # eq
    # hash
    # init
    # repr
    # setattr


@dataclass
class PacketWrapper:
    """
    Class that contains multiple Packets with the same id

    This class contains all the packets that are being originated by the same
    ip and port of origin and responder hosts.

    Args:
        id (str): a combination of the ip and port of origin and responder host
        packets (list[Packet]): list of the packets excanged by the hosts according
            that port
    """
    id: str
    packets: list[Packet] = field(default_factory=list)

    def add_packet(self, p: Packet):
        """
        adds the packet p to the list only if the id is equal to the
        id of the object

        Args:
            p (Packet): the packet to be added to this wrapper

        Raises:
            KeyError: raises a KeyError if the id of the packet doesn't match
        """
        if p.generate_id() == self.id:
            self.packets.append(p)
        else:
            raise KeyError
    
    def to_json_obj(self) -> object:
        """
        Convert this object to an object that can be easily converted to a json

        Returns:
            object: this object as a dumpable object
        """
        packets = []
        for packet in self.packets:
            packets.append(packet.to_json_obj())

        return {
            "id": self.id,
            "packets": packets,
        }

    # eq
    # init
    # repr


class PacketController:
    """
    Class that contains the method used to filter and organize packets

    Args:
        path_of_file_input (str): path of the file that contains the logs to be acquired
        path_of_file_output (str): path of the file where the preprocessed lines are stored or will be stored
        path_of_file_json (str): path of the file where to write the json file
        lines_to_remove (list): list of the lines to remove from the log file
        lines_to_remove_ash (list): list of the # to remove from the file
        strings_to_filter_rows (list): list of string to be filtered out
    """
    def __init__(self, 
        path_of_file_input: str,
        path_of_file_output: str='',
        path_of_file_json: str='',
        lines_to_remove: list=[],
        lines_to_remove_ash: list=[],
        strings_to_filter_rows: list=[]) -> None:
        self.path_of_file_input = path_of_file_input
        self.path_of_file_output = path_of_file_output
        self.path_of_file_json = path_of_file_json
        self.lines_to_remove = lines_to_remove
        self.lines_to_remove_ash = lines_to_remove_ash
        self.strings_to_filter_rows = strings_to_filter_rows
        self.packetWrapper_list = [] # list of packet wrapper from preprocessed lines
        pass
    
    def load_paths_and_filters_from_config_file(self, config_file_path):
        '''loads all path and filters form the ini file'''
        import configparser
        print('reading config option from file...')
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # checks if Files is in config.ini file
        if 'Files' in config:
            self.path_of_file_output = config['Files']['path_of_file_output'] if 'path_of_file_output' in config['Files'] else ''
            self.path_of_file_json = config['Files']['path_of_file_json']  if 'path_of_file_json' in config['Files'] else ''
        else:
            self.path_of_file_output = ''
            self.path_of_file_json = ''

        # checks if Filters is in config.ini file
        if 'Filters' in config:
            self.lines_to_remove = config['Filters']['lines_to_remove']  if 'lines_to_remove' in config['Filters'] else ''
            self.lines_to_remove_ash = config['Filters']['lines_to_remove_ash']  if 'lines_to_remove_ash' in config['Filters'] else ''
            self.strings_to_filter_rows = config['Filters']['strings_to_filter_rows']  if 'strings_to_filter_rows' in config['Filters'] else ''

            self.lines_to_remove = self.lines_to_remove.replace('\'', '').split(',')
            self.lines_to_remove_ash = self.lines_to_remove_ash.replace('\'', '').split(',')
            self.strings_to_filter_rows = self.strings_to_filter_rows.replace('\'', '').split(',')
        else:
            self.lines_to_remove = '' 
            self.lines_to_remove_ash = '' 
            self.strings_to_filter_rows = '' 

        print('...reading complete')


    def open_stored_preprocessed_lines(self) -> list:
        '''read stored preprocessed lines from a file specified in the
           path_of_file_output of this object'''
        print('reading stored lines from file...')
        with open(self.path_of_file_output, 'r') as f:
            preprocessed_lines = []
            for line in f:
                preprocessed_lines.append(line)

            print('...reading complete')
            return preprocessed_lines

    def print_preprocessed_lines_to_file(self, preprocessed_lines: list):
        '''prints preprocessed lines to a file specified in the path_of_file_output
           field of this object'''
        print('printing preprocessed lines to file...')
        with open(self.path_of_file_output, 'w') as f_out:
            # writing lines to new file
            for line in preprocessed_lines:
                f_out.write(line)
        print('...printing complete')

    def normalize_lines(self) -> list:
        '''normalize lines from file and if the path_of_file_output
           is set, prints the lines to a file'''
        print('normalizing lines...')
        preprocessed_lines = []
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
                    preprocessed_lines.append(line)
        print('...normalization completed')
        return preprocessed_lines

    def conv_lines_to_PacketWrapper_list(self, preprocessed_lines: list) -> list:
        '''Wrappes a list of preprocessed lines to a list of PacketWrapper'''
        print('converting preprocessed lines to list of packet wrappers...')
        packets = self.__conv_lines_to_list_of_Packet(preprocessed_lines)
        
        packetWrapper_dict = {}
        for p in packets:
            id = p.generate_id()

            if id not in packetWrapper_dict:
                packetWrapper_dict[id] = PacketWrapper(id, [p])
            else:
                packetWrapper_dict[id].add_packet(p)
        print('...conversion completed')
        self.packetWrapper_list = list(packetWrapper_dict.values())
        return self.packetWrapper_list
        
    def __conv_lines_to_list_of_Packet(self, preprocessed_lines: list) -> list:
        '''converts a list of preprocessed lines to a list of Packets'''
        packets = []
        
        for line in preprocessed_lines:
            packets.append(self.__conv_conn_line_to_Packet(line))

        return packets

    def __conv_conn_line_to_Packet(self, line: str) -> Packet:
        '''converts a conn.log line to a Packet'''
        list_to_pack = line.split('\t')

        # getting info to insert in Packet
        uid = list_to_pack[1]
        orig_ip = list_to_pack[2]
        orig_port = list_to_pack[3]
        resp_ip = list_to_pack[4]
        resp_port = list_to_pack[5]
        ts = list_to_pack[0]
        services = list_to_pack[7]
        state = list_to_pack[11]

        return Packet(uid, orig_ip, orig_port, resp_ip, resp_port, ts, services, state)
        
    def print_packetWrapper_list_to_json_file(self):
        '''prints all the packetwrapper list to a json file'''
        print('writing the list of packet to a json file...')
        with open(self.path_of_file_json, 'w') as f:
            to_json = []
            for pw in self.packetWrapper_list:
                to_json.append(pw.to_json_obj())
            
            json.dump(to_json, f, indent=4)
        print('...writing completed')




