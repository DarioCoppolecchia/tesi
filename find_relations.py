from datetime import datetime
import csv

def getId(pkt, h):
    return f"{pkt[h['id.orig_h']]}  {pkt[h['id.orig_p']]}   {pkt[h['id.resp_h']]}   {pkt[h['id.resp_p']]}"

def timestamp_diff(arr):
    time_arr = [int(float(elem)) for i, elem in enumerate(arr) if i % 2 == 1]
    time_arr.sort()
    diff = 0
    for i in range(len(time_arr) - 1):
        diff += time_arr[i + 1] - time_arr[i]
    return diff / (len(time_arr) - 1)
    
def time_to_str(time):
    return datetime.utcfromtimestamp(time).strftime('%H:%M:%S')

def get_file_dict(log_file_path: str) -> dict:
    with open(log_file_path, 'r') as f_log:
        csvr = csv.reader(f_log, delimiter="\t")
        header = next(csvr)
        header_pos = {h: i for i, h in enumerate(header)}
        # filling the dict of connections with packets
        file_dict = {}
        for i, pkt in enumerate(csvr):
            try:
                id = getId(pkt, header_pos)
            except:
                try: 
                    id = pkt[header_pos['fuid']]
                except:
                    id = pkt[header_pos['id']]
            if id in file_dict:
                file_dict[id].append(pkt)
            else:
                file_dict[id] = [pkt]
        return file_dict, header_pos

def check_param(param_to_check: str, file_dict: dict, header_pos: list):
    # gather all the param of every connection
    param_dict = {}
    for conn, pkts in file_dict.items():
        for pkt in pkts:
            if conn in param_dict:
                if pkt[header_pos[param_to_check]] not in param_dict[conn]:
                    param_dict[conn].append(pkt[header_pos[param_to_check]])
                    param_dict[conn].append(pkt[header_pos['ts']])
            else:
                param_dict[conn] = [pkt[header_pos[param_to_check]], pkt[header_pos['ts']]]
    return param_dict

def print_checked_param(param_to_print: str, param_dict: dict):
    with open("./outputs/redundant_attr_conn/" + param_to_print + ".txt", 'w') as f:
        min_diff = 86400
        max_rico = 0
        count = 0
        for conn, param_arr in param_dict.items():
            n = len(param_arr) / 2
            if n > 1:
                diff = timestamp_diff(param_arr)
                if min_diff > diff:
                    min_diff = diff
                if max_rico < n:
                    max_rico = n
                f.write(f'per questo id {conn} ci sono {n} ricorrenze, con differenza di tempo media {time_to_str(diff)}: {param_arr}\n')
                count += 1

        print(f"numero ricorrenze: {count}\nmax ricorrenza: {max_rico}\nmin differenza: {min_diff}")

def print_list_to_file(file_path, file_name, list):
    # creates output directory if doesn't exists
    import os
    os.makedirs(file_path, exist_ok=True)

    # prints to file
    with open(file_path + file_name, 'w') as f:
        for c in list:
            f.write(f"{c}\n")

def find_correlations_conn_column(file_dict_conn: dict, header_pos_conn: dict, file_dict_value: dict, column: str, value: str):
    corr_found = set()
    corr_not_found = set()
    val_found = set()
    for conn, val in file_dict_conn.items():
        for c in val:
            value_to_cmp = c[header_pos_conn[column]].split(',')
            for v in value_to_cmp:
                val_found.add(v)
            if value in value_to_cmp:
                id = getId(c, header_pos_conn)
                to_print = f"{conn}: {c}"
                if id in file_dict_value:
                    corr_found.add(to_print)
                else:
                    corr_not_found.add(to_print)
    return corr_found, corr_not_found, val_found

def get_all_values_of_columns(cols, file_dict, header_pos) -> set:
    values = set()
    for _, v in file_dict.items():
        for c in v:
            val = ''
            for col in cols:
                for s in c[header_pos[col]].split(','):
                    val += s + " "
            values.add(val)
    return values

def count_ric_val_col(filepath, col):
    col_val = {}
    with open(filepath) as f:
        csvr = csv.reader(f, delimiter="\t")
        header = next(csvr)
        header_pos = {h: i for i, h in enumerate(header)}
        for line in csvr:
            index = line[header_pos[col]]
            if index not in col_val:
                col_val[index] = 1
            else:
                col_val[index] += 1
    new_dict = {}
    for k, v in col_val.items():
        if v > 1:
            new_dict[k] = v
    return new_dict

column = 'version'
value_to_check = '-'
conn_file_path = "./logs/conn.log"
value_file_path = "./logs/ssl.log"
param_to_check = 'proto'
file_dict_conn, header_pos_conn = get_file_dict(conn_file_path)
#file_dict_value, header_pos = get_file_dict(value_file_path)
#corr_found, corr_not_found, val_found = find_correlations_conn_column(file_dict_conn, header_pos_conn, file_dict_value, column, value_to_check)
#print(val_found)
#print_list_to_file(f"outputs/correlations_between_files_{column}/", f"corr_found_{value_to_check}.txt", corr_found)
#print_list_to_file(f"outputs/correlations_between_files_{column}/", f"corr_not_found_{value_to_check}.txt", corr_not_found)

#res = get_all_values_of_columns(['curve'], file_dict_conn, header_pos_conn)
#for r in res:
#   print(r)

#print(count_ric_val_col('./logs/ocsp.log', 'id'))

#for h in header_pos_conn:
#    print(h)

#param_dict = check_param(param_to_check, file_dict_conn, header_pos_conn)
#print_checked_param(param_to_check, param_dict)
