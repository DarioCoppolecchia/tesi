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
            self.traces_controller.lines_to_remove_ash = self.__get_lines_from_input('the line to add to the list of lines where to remove the start of the line')
            self.traces_controller.strings_to_filter_event = self.__get_lines_from_input('the string to add to the list of strings to filter out')
            self.traces_controller.path_of_file_input = input('type the path of the file containing the lines of the connections to analyze\n> ')
            self.traces_controller.path_of_file_output = input('the path of the file that will contain the preprocessed lines (optional)\n> ')
            self.traces_controller.path_of_file_json = input('the path of the json file where to store the json of the list of NetworkConversation (optional)\n> ')

    def main_loop(self):
        """
        main loop of the application containig the UI elements that control the NetworkTrafficController
        for every iteration this allows the user to do one of the following operations:
            #. apply label to log file stored in path_of_file_input (at the moment, only works for tuesday)
            #. read and normalize lines from the file stored in path_of_file_input
            #. print preprocessed lines to a file
            #. convert normalized lines to a Traces list
            #. print traces list to a json file
            #. open stored preprocessed lines
            #. loads configuration options from config.ini file
            #. show configuration options
            #. modify the path of input file
            #. modify the path of preprocessed lines
            #. modify the path of json file
            #. exit program
        """
        while True:
            op = input("""\ntype the number for the various options:
    1) apply label to log file stored in path_of_file_input (at the moment, only works for tuesday)
    2) read and normalize lines from the file stored in path_of_file_input
    3) print preprocessed lines to a file
    4) convert normalized lines to a Traces list
    5) print traces list to a json file
    6) open stored preprocessed lines
    7) loads configuration options from config.ini file
    8) show configuration options
    9) modify the path of input file
    10) modify the path of preprocessed lines
    11) modify the path of json file
    12) exit program\n> """)
            os.system('clear')

            if op == "1":
                import time
                import datetime
                constraint_to_label = [
                    {
                        'lower_bound': time.mktime(datetime.datetime.strptime("2017-07-04 14:18:00", '%Y-%m-%d %H:%M:%S').timetuple()),
                        'upper_bound': time.mktime(datetime.datetime.strptime("2017-07-04 15:22:00", '%Y-%m-%d %H:%M:%S').timetuple()),
                        'ip_attacker': '172.16.0.1',
                        'ip_attacked': '192.168.10.50',
                        'label': 'FTP-Patator',
                    },
                    {
                        'lower_bound': time.mktime(datetime.datetime.strptime("2017-07-04 19:18:00", '%Y-%m-%d %H:%M:%S').timetuple()),
                        'upper_bound': time.mktime(datetime.datetime.strptime("2017-07-04 20:22:00", '%Y-%m-%d %H:%M:%S').timetuple()),
                        'ip_attacker': '172.16.0.1',
                        'ip_attacked': '192.168.10.50',
                        'label': 'SSH-Patator',
                    },
                ]
                self.traces_controller.apply_label_to_events_in_file(constraint_to_label)
            elif op == "2":
                self.traces_controller.normalize_lines()
            elif op == "3":
                self.traces_controller.print_preprocessed_lines_to_file()
            elif op == "4":
                self.traces_controller.conv_lines_to_Trace_list()
            elif op == "5":
                self.traces_controller.print_Trace_list_to_json_file()
            elif op == "6":
                self.traces_controller.open_stored_preprocessed_lines()
            elif op == "7":
                config_path = input('type the path of the config.ini file\n> ')
                self.traces_controller.load_paths_and_filters_from_config_file(config_path)
            elif op == "8":
                print("list of lines where to remove the word with #:")
                for line in self.traces_controller.lines_to_remove_ash:
                    print('   ' + line)
                print("list of string to filter out:")
                for line in self.traces_controller.strings_to_filter_event:
                    print('   ' + line)
                print("path of the file containing the lines of the packets to analyze: " + self.traces_controller.path_of_file_input)
                print("path of the file that will contain the preprocessed lines: " + self.traces_controller.path_of_file_output)
                print("path of the json file where to store the json of the list of NetworkConversation: " + self.traces_controller.path_of_file_json)
            elif op == "9":
                self.traces_controller.path_of_file_input = input('type the path of the file containing the lines of the packets to analyze\n> ')
            elif op == "10":
                self.traces_controller.path_of_file_output = input('the path of the file that will contain the preprocessed lines (optional)\n> ')
            elif op == "11":
                self.traces_controller.path_of_file_json = input('the path of the json file where to store the json of the list of NetworkConversation (optional)\n> ')
            elif op == "12":
                if input('are you sure you want to exit? (y or Y):\n> ').lower() == 'y':
                    return
            else:
                print('command not valid, enter an integer number between 1 and 11')
    
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
            
        os.system('clear')
        return lines