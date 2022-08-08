# importing pandas library
import json
import csv
import os

class PacketController:
    '''class that contains the method used to filter and organize packets'''
    def __init__(self, 
        path_of_file_input: str, 
        path_of_file_output: str,
        path_of_file_json: str, 
        path_of_temp_json_file: str, 
        lines_to_remove: list, 
        lines_to_remove_ash: list,
        strings_to_filter_rows: list,
        to_file=False) -> None:
        self.path_of_file_input = path_of_file_input
        self.path_of_file_output = path_of_file_output
        self.path_of_file_json = path_of_file_json
        self.path_of_temp_json_file = path_of_temp_json_file
        self.lines_to_remove = lines_to_remove
        self.lines_to_remove_ash = lines_to_remove_ash
        self.strings_to_filter_rows = strings_to_filter_rows
        self.to_file = to_file
        pass

    def tsv_line_to_dict(row, keys):
        # creating object to be dumped and writteon on disk
        conn_temp = {}
        for i in range(len(keys)):
            conn_temp[keys[i]] = row[i]

        return conn_temp

    def normalize_lines():
