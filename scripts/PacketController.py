# importing pandas library
import json
from operator import truediv
from PacketWrapper import PacketWrapper
from Packet import Packet

class PacketController:
    '''class that contains the method used to filter and organize packets'''
    def __init__(self, 
        path_of_file_input: str,
        path_of_file_output: str='',
        path_of_file_json: str='',
        lines_to_remove: list=[],
        lines_to_remove_ash: list=[],
        strings_to_filter_rows: list=[],
        to_file: bool=False,
        path_of_stored_lines: str='') -> None:
        self.path_of_file_input = path_of_file_input
        self.path_of_file_output = path_of_file_output
        self.path_of_file_json = path_of_file_json
        self.lines_to_remove = lines_to_remove
        self.lines_to_remove_ash = lines_to_remove_ash
        self.strings_to_filter_rows = strings_to_filter_rows
        self.to_file = to_file
        self.path_of_stored_lines = path_of_stored_lines
        self.packetWrapper_list = [] # list of packet wrapper from preprocessed lines
        pass
    
    def load_paths_and_filters_from_config_file(self, config_file_path):
        '''loads all path and filters form the ini file'''
        import configparser
        print('reading config option from file...')
        config = configparser.ConfigParser()
        config.read(config_file_path)
        self.path_of_file_output = config['Files']['path_of_file_output']
        self.path_of_file_json = config['Files']['path_of_file_json']
        self.path_of_temp_json_file = config['Files']['path_of_temp_json_file']
        self.lines_to_remove = config['Filters']['lines_to_remove'].replace('\'', '').split(',')
        self.lines_to_remove_ash = config['Filters']['lines_to_remove_ash'].replace('\'', '').split(',')
        self.strings_to_filter_rows = config['Filters']['strings_to_filter_rows'].replace('\'', '').split(',')
        print('...reading complete')


    def open_stored_preprocessed_lines(self) -> list:
        print('reading stored lines from file...')
        with open(self.path_of_stored_lines, 'r') as f:
            preprocessed_lines = []
            for line in f:
                preprocessed_lines.append(line)

            print('...reading complete')
            return preprocessed_lines

    def print_preprocessed_lines_to_file(self, preprocessed_lines: list):
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
        print('converting preprocessed lines to list of packet wrappers...')
        packets = self.conv_lines_to_list_of_Packet(preprocessed_lines)
        
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
        
    def conv_lines_to_list_of_Packet(self, preprocessed_lines: list) -> list:
        packets = []
        
        for line in preprocessed_lines:
            packets.append(self.conv_line_to_Packet(line))

        return packets

    def conv_line_to_Packet(self, line: str) -> Packet:
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
        print('writing the list of packet to a json file...')
        with open(self.path_of_file_json, 'w') as f:
            to_json = []
            for pw in self.packetWrapper_list:
                to_json.append(pw.to_json_obj())
            
            json.dump(to_json, f, indent=4)
        print('...writing completed')


