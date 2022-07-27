# importing pandas library
import json
import csv

path_of_file_input  = '../logs/connections.log'
path_of_file_output = '../logs/connections.tsv'
path_of_file_json   = '../logs/connections.json'

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

lines_to_remove_ash = [
    '#fields\t',
]

strings_to_filter_rows = [
    'SaveConn::',
    '(empty)',
    'connection.',
]

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

# inefficient
'''
with open(path_of_file_output, "r") as f:
    reader = csv.reader(f, delimiter="\t")
    connections = {}
    for i, line in enumerate(reader):

        # grouping connections for orig-resp
        #for line in connections_log:

        keys_to_ignore = [
            'orig', 
            'resp',
        ]

        keys = []

        for key in connections_log:
            if key not in keys_to_ignore:
                keys.append(key)

        for _, row in connections_log.iterrows():
            conn_key = row['orig'] + ' ' + row['resp']
            if conn_key not in connections:
                connections[conn_key] = []

            conn_temp = {}
            for key in keys:
                conn_temp[key] = row[key]
                
            connections[conn_key].append(conn_temp)
            

        for conn in connections:
            print('\n' + conn + ':')
            for i in connections[conn]:
                print('\t' + str(i))
'''

# hopefully efficient but with ordered data
with open(path_of_file_output, "r") as f_in:
    with open(path_of_file_json, "w") as f_out:
        reader = csv.reader(f_in, delimiter="\t")
        f_out.write('{')

        # get the header
        keys = []
        for row in reader:
            keys = row
            break

        count = 0
        prev_key = '' # used to know when a new connection is incoming
        for row in reader:
            key = row[0] + " " + row[1]
            if prev_key != key:
                prev_key = key
                if count > 0:
                    f_out.write("], ")
                count += 1

                f_out.write("\"" + key + "\": [")
            else:
                f_out.write(', ')
            
            conn_temp = {}
            # creating object
            for i in range(len(keys)):
                conn_temp[keys[i]] = row[i]

            # dumping in json

            f_out.write(json.dumps(conn_temp))

        f_out.write(']}')
            







# dumping to json 

#with open(path_of_file_json, 'w') as f:
    #pass
    #json.dump(connections, f)
        