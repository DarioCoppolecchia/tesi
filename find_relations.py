from datetime import datetime
import csv

# creates output directory if doesn't exists
import os
path = [
    './outputs/correlations_between_files/', 
    './outputs/redundant_attr_conn/',
]
for p in path:
    os.makedirs(p, exist_ok=True)


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

def get_file_dict(log_file_path: str="./logs/conn.log") -> dict:
    with open(log_file_path, 'r') as f_log:
        csvr = csv.reader(f_log, delimiter="\t")
        header = next(csvr)
        header_pos = {h: i for i, h in enumerate(header)}

        # filling the dict of connections with packets
        file_dict = {}
        for i, pkt in enumerate(csvr):
            id = getId(pkt, header_pos)
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

def find_correlations_conn_service(file_dict_conn: dict, header_pos_conn: dict, file_dict_service: dict, header_pos_service: dict, service: str):
    corr_found = []
    corr_not_found = []
    for conn, val in file_dict_conn.items():
        for c in val:
            if service in c[header_pos_conn['service']].split(','):
                if getId(c, header_pos_conn) in file_dict_service:
                    corr_found.append(f"{conn}: {val}")
                else:
                    corr_not_found.append(f"{conn}: {val}")
    with open(f'outputs/correlations_between_files/corr_found_{service}.txt', 'w') as f:
        for c in corr_found:
            f.write(f"{c}\n")
    with open(f'outputs/correlations_between_files/corr_not_found_{service}.txt', 'w') as f:
        for c in corr_not_found:
            f.write(f"{c}\n")

def get_all_values_of_column(col, file_dict, header_pos) -> set:
    values = set()
    for _, v in file_dict.items():
        for c in v:
            for s in c[header_pos[col]].split(','):
                values.add(s)
    return values

service_to_check = 'ntlm'
conn_file_path = "./logs/conn.log"
service_file_path = "./logs/ntlm.log"
param_to_check = 'proto'
file_dict_conn, header_pos_conn = get_file_dict(conn_file_path)
file_dict_service, header_pos_service = get_file_dict(service_file_path)
find_correlations_conn_service(file_dict_conn, header_pos_conn, file_dict_service, header_pos_service, service_to_check)

#print(get_all_values_of_column('service', file_dict_conn, header_pos_conn))

#param_dict = check_param(param_to_check, file_dict_conn, header_pos_conn)
#print_checked_param(param_to_check, param_dict)