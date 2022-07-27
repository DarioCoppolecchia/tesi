# importing pandas library
import json
import csv
import os

# paths of the different files
path_of_file_input  = '../logs/connections.log'
path_of_file_output = '../logs/connections.tsv'
path_of_file_json   = '../logs/connections.json'
path_of_temp_json_file = '../logs/connection_'

# start of the lines to be totally removed
lines_to_remove = [
    '#separator',
    '#set_separator',
    '#empty_field',
    '#unset_field',
    '#path',
    '#open',
    '#close',
    '#types',
]

# start of the lines to replaced with ""
lines_to_remove_ash = [
    '#fields\t',
]

# strings to be filtered out
strings_to_filter_rows = [
    'SaveConn::',
    '(empty)',
    'connection.',
]

print('normalizing lines...')
# normalizing lines
with open(path_of_file_input, "r+") as f_in:
    with open(path_of_file_output, 'w') as f_out:
        for line in f_in:
            # removing comment lines
            to_remove = False
            for line_to_check in lines_to_remove:
                if line.startswith(line_to_check):
                    to_remove = True
            if not(to_remove):
                # replacing comment in field/types lines
                for line_to_check in lines_to_remove_ash:
                    if line.startswith(line_to_check):
                        line = line.replace(line_to_check, '')
                        break

                # removing unnecessary strings
                for string in strings_to_filter_rows: 
                    line = line.replace(string, '')

                # writing lines to new file
                f_out.write(line)
os.remove(path_of_file_input)

print('...normalizations completed')

# printing the connections in a json file
# memory inefficient with unordered data
'''
with open(path_of_file_output, "r") as f:
    # create reader and start of the json file
    reader = csv.reader(f, delimiter="\t")
    connections = {}
    # for every row
    for i, line in enumerate(reader):

        # grouping connections for orig-resp
        #for line in connections_log:

        keys_to_ignore = [
            'orig', 
            'resp',
        ]

        # keys of the file
        keys = []
        for key in connections_log:
            if key not in keys_to_ignore:
                keys.append(key)

        
        for _, row in connections_log.iterrows():
            # create the key
            conn_key = row['orig'] + ' ' + row['resp']

            # if the connection hasn't been found yet create
            # the key in the dictionary
            if conn_key not in connections:
                connections[conn_key] = []

            # create object to be written
            conn_temp = {}
            for key in keys:
                conn_temp[key] = row[key]
                
            # append the packet to the connection
            connections[conn_key].append(conn_temp)

        # print every connection
        for conn in connections:
            print('\n' + conn + ':')
            for i in connections[conn]:
                print('\t' + str(i))
            
        # dumping in json
        f_out.write(json.dumps(conn_temp))
'''

def tsv_line_to_dict(row, keys):
    # creating object to be dumped and writteon on disk
    conn_temp = {}
    for i in range(len(keys)):
        conn_temp[keys[i]] = row[i]

    return conn_temp

'''
# memory efficient but with ordered data
with open(path_of_file_output, "r") as f_in:
    with open(path_of_file_json, "w") as f_out:
        # create reader and start of the json file
        reader = csv.reader(f_in, delimiter="\t")
        f_out.write('{')

        # get the header
        keys = []
        for row in reader:
            keys = row
            break

        count = 0
        prev_key = '' # used to know when a new connection is incoming

        # for every row
        for row in reader:
            # get the key
            key = row[0] + " " + row[1]
            # check if the key has already been seen
            if prev_key != key:
                prev_key = key

                # if it's not the first cicle, print the parenthesis
                if count > 0:
                    f_out.write("], ")
                count += 1

                # print the key if the key has changed
                f_out.write("\"" + key + "\": [")
            else:
                # if it's hasn't changed, just print the ", "
                f_out.write(', ')
            
            conn_temp = tsv_line_to_dict(row, keys)

            # dumping in json
            f_out.write(json.dumps(conn_temp))

        # writing the end of the file
        f_out.write(']}')
'''

print('creating the temporary files...')
            
# memory efficient with non ordered data
# (using more file to be then regrouped into one)
with open(path_of_file_output, "r") as f_in:
    connections_keys = []

    # create reader and start of the json file
    reader = csv.reader(f_in, delimiter="\t")

    # get the header
    keys = []
    for row in reader:
        keys = row
        break

    # cycle the lines in the tsv file
    for row in reader:
        # get the key
        key = row[0] + " " + row[1]
        
        # open the corrispondent file of the key
        with open(path_of_temp_json_file + key + '.json', 'a') as f_temp:

            # check if the key hasn't been found before
            if key not in connections_keys:
                # append the list of keys found
                connections_keys.append(key)

                # write the start of the list if key is new
                f_temp.write('[')
            else:
                # if it's hasn't changed, just print the ", "
                f_temp.write(',\n')

            conn_temp = tsv_line_to_dict(row, keys)

            # dumping in json
            f_temp.write(json.dumps(conn_temp))
os.remove(path_of_file_output)

print('...temporary files created')

print('merging files...')

with open(path_of_file_json, "w") as f_out:
    # writing the start of the JSON
    f_out.write('{')

    # reading from all the files to create the main file
    # with all the connections (deleting the files one at a time)
    count = 0
    for key in connections_keys:
        path = path_of_temp_json_file + key + '.json'

        with open(path, 'r') as f:
            if count > 0:
                f_out.write("], ")
            count += 1

            # writing the key
            f_out.write("\"" + key + "\": ")
            for line in f:
                line = line.replace('\n', '')
                f_out.write(line)
        
        # removing file from disk after reading it
        os.remove(path)

    # writing the end of the file
    f_out.write(']}')

print('...file merged')
