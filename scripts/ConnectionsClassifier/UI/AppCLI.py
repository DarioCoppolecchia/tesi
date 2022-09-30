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
    3) exit program\n> """)
            os.system('cls' if os.name == 'nt' else 'clear')
            if op == "1":
                self.traces_controller.normalize_lines()
            elif op == "2":
                self.traces_controller.print_Trace_list_to_json_file()
            elif op == "3":
                res = input('are you sure you want to exit? (y or Y or just enter a blank line):\n> ')
                if res == '' or res.lower() == 'y':
                    return
            else:
                print('command not valid, enter an integer number between 1 and 3')
    
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