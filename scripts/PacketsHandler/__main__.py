from PacketsModule.Packets import PacketController
import os

class Main:
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
        self.pc = PacketController()

        if config_path != '':
            self.pc.load_paths_and_filters_from_config_file(config_path)
        else:
            print('path of the config file not given, enter config options manually:')
            self.pc.lines_to_remove = self.__get_lines_from_input('the line to add to the list of lines to remove')
            self.pc.lines_to_remove_ash = self.__get_lines_from_input('the line to add to the list of lines where to remove the start of the line')
            self.pc.strings_to_filter_rows = self.__get_lines_from_input('the string to add to the list of strings to filter out')
            self.pc.path_of_file_input = input('type the path of the file containing the lines of the packets to analyze\n> ')
            self.pc.path_of_file_output = input('the path of the file that will contain the preprocessed lines (optional)\n> ')
            self.pc.path_of_file_json = input('the path of the json file where to store the json of the list of PacketWrapper (optional)\n> ')

    def main_loop(self):
        """
        main loop of the application containig the UI elements that control the PacketController
        """
        while True:
            op = input("""\ntype the number for the various options: 
 1) read and normalize lines from the file stored in path_of_file_input
 2) print preprocessed lines to a file
 3) convert normalized lines to a PacketWrapper list
 4) print packet wrapper list to a json file
 5) open stored preprocessed lines
 6) loads configuration options from config.ini file
 7) show configuration options
 8) modify the path of input file
 9) modify the path of preprocessed lines
 10) modify the path of json file
 11) exit program\n> """)
            os.system('clear')

            if op == "1":
                self.pc.normalize_lines()
            elif op == "2":
                self.pc.print_preprocessed_lines_to_file()
            elif op == "3":
                self.pc.conv_lines_to_PacketWrapper_list()
            elif op == "4":
                self.pc.print_packetWrapper_list_to_json_file()
            elif op == "5":
                self.pc.open_stored_preprocessed_lines()
            elif op == "6":
                config_path = input('type the path of the config.ini file\n> ')
                self.pc.load_paths_and_filters_from_config_file(config_path)
            elif op == "7":
                print("list of lines to remove:")
                for line in self.pc.lines_to_remove:
                    print('   ' + line)
                print("list of lines where to remove the word with #:")
                for line in self.pc.lines_to_remove_ash:
                    print('   ' + line)
                print("list of string to filter out:")
                for line in self.pc.strings_to_filter_rows:
                    print('   ' + line)
                print("path of the file containing the lines of the packets to analyze: " + self.pc.path_of_file_input)
                print("path of the file that will contain the preprocessed lines: " + self.pc.path_of_file_output)
                print("path of the json file where to store the json of the list of PacketWrapper: " + self.pc.path_of_file_json)
            elif op == "8":
                self.pc.path_of_file_input = input('type the path of the file containing the lines of the packets to analyze\n> ')
            elif op == "9":
                self.pc.path_of_file_output = input('the path of the file that will contain the preprocessed lines (optional)\n> ')
            elif op == "10":
                self.pc.path_of_file_json = input('the path of the json file where to store the json of the list of PacketWrapper (optional)\n> ')
            elif op == "11":
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

if __name__ == "__main__":
    Main('config.ini')