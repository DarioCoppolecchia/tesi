from calendar import c
from cmath import inf
from datetime import datetime
import csv

file_conn_path = "./logs/conn.log"

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

with open(file_conn_path, 'r') as f_conn:
    csvr = csv.reader(f_conn, delimiter="\t")
    header = next(csvr)
    header_pos = {h: i for i, h in enumerate(header)}

    # filling the dict of connections with packets
    conn_dict = {}
    for i, pkt in enumerate(csvr):
        id = getId(pkt, header_pos)
        if id in conn_dict:
            conn_dict[id].append(pkt)
        else:
            conn_dict[id] = [pkt]

    # gather all the proto of every connection
    param_to_check = 'tunnel_parents'
    param_dict = {}
    for conn, pkts in conn_dict.items():
        for pkt in pkts:
            if conn in param_dict:
                if pkt[header_pos[param_to_check]] not in param_dict[conn]:
                    param_dict[conn].append(pkt[header_pos[param_to_check]])
                    param_dict[conn].append(pkt[header_pos['ts']])
            else:
                param_dict[conn] = [pkt[header_pos[param_to_check]], pkt[header_pos['ts']]]
        
    with open("./outputs/" + param_to_check + ".txt", 'w') as f:
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
