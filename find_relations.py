from datetime import datetime
import csv
from random import random
import tqdm

def getId(pkt, h):
    return f"{pkt[h['id.orig_h']]}  {pkt[h['id.orig_p']]}   {pkt[h['id.resp_h']]}   {pkt[h['id.resp_p']]}"

def getId_from_cols(pkt, h, cols):
    output = ""
    for col in cols:
        output += f"{pkt[h[col]]} "
    return output[:-1]

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
                id = getId_from_cols(pkt, header_pos, ['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto'])
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
                    val += s + "\t"
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

def get_values_of_columns(id_list: list, cols: list, file_dict: dict, header_pos: dict) -> list:
    out_l = []
    for k, v in file_dict.items():
        for conn in v:
            sub_l = [k]
            for col in cols:
                sub_l.append(conn[header_pos[col]])
            out_l.append('\t'.join(sub_l))
    out_l.insert(0, "\t".join(([','.join(id_list)] + cols)))
    return out_l

def get_n_values_of_columns(cols: list, n: int, file_dict: dict, header_pos: dict):
    values = []
    for i, (_, v) in enumerate(file_dict.items()):
        val = []
        for col in cols:
            val.append(v[0][header_pos[col]])
        values.append(val)
        if i >= n:
            break
    return values

def get_n_combinations_of_values_of_columns(cols: list, file_dict: dict, header_pos: dict):
    values = {}
    for _, v in file_dict.items():
        val = []
        for col in cols:
            val.append(v[0][header_pos[col]])
        key = ",".join(val)
        if key in values:
            values[key][-1] += 1
        else:
            values[key] = val + [1] 

    ret = []
    for _, v in values.items():
        ret.append(v)
    return ret

def get_number_of_occurrencies_of_cols_from_file(log_file_path: str, cols: list) -> dict:
    with open(log_file_path, 'r') as f_log:
        csvr = csv.reader(f_log, delimiter="\t")
        header = next(csvr)
        header_pos = {h: i for i, h in enumerate(header)}
        # filling the dict of connections with packets
        file_dict = {}
        for pkt in csvr:
            try:
                id = getId_from_cols(pkt, header_pos, cols)
            except:
                try: 
                    id = pkt[header_pos['fuid']]
                except:
                    id = pkt[header_pos['id']]
            if id in file_dict:
                file_dict[id] += 1
            else:
                file_dict[id] = 1
        return file_dict

def clean_files(files_to_clean_path: list):
    for file in files_to_clean_path:
        print(f'cleaning: {file}')
        lines = []
        with open(file, 'r') as f:
            lines = f.readlines()
            del lines[:6]
            del lines[1]
            del lines[-1]
            lines[0] = lines[0].replace("#fields\t", "")
        with open(file, 'w') as f:
            f.writelines(lines)
        

def copy_contents_of_files_into_another_file(input_files_path: list, output_file_path: str):
    with open(output_file_path, 'w') as f_out:
        for input_path in input_files_path:
            with open(input_path, 'r') as f_in:
                f_out.writelines(f_in.readlines())

'''
Il parametro sottostante è un array di oggetti dove ognuno contiene il limite inferiore, il limite superiore, l'ip dell'attaccante, 
l'ip dell'attaccato e la label corrispondente

label(x) <- 
    lower_bound <= x.ts <= upper_bound && 
    ip_attacker = x.ip_orig && 
    ip_attacked = x.ip_resp

struttura della lista
interval_to_label = [
    { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
    { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
    ...
    { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
]
'''
def apply_label_to_events_in_file(input_files_path: str, output_file_path: str, header_pos: list, constraint_to_label: list):
    with open(output_file_path, 'w') as f_out:
        with open(input_files_path, 'r') as f_in:
            next(f_in)
            for line in f_in:
                line = line.replace('\n', '')
                splitted = line.split('\t')
                ts = splitted[header_pos['ts']]
                orig_ip = splitted[header_pos['id.orig_h']]
                resp_ip = splitted[header_pos['id.resp_h']]
                for constraints in constraint_to_label:
                    if (float(constraints['lower_bound']) <= float(ts) <= float(constraints['upper_bound']) and 
                        constraints['ip_attacker'] == orig_ip and
                        constraints['ip_attacked'] == resp_ip):
                        line += '\t' + constraints['label']
                        break
                else:
                    line += '\t' + 'BENIGN'
                f_out.write(line + '\n')

def print_file_dict_to_file(output_file_path: str, file_dict: dict, header_pos: dict):
    import json
        
    with open(output_file_path + '_dict.json', "w") as outfile:
        json.dump(file_dict, outfile)
    with open(output_file_path + '_header.json', "w") as outfile:
        json.dump(header_pos, outfile)

def read_file_dict_from_file(input_file_path: str):
    import json

    with open(input_file_path + '_dict.json') as f:
        file_dict = json.load(f)
    with open(input_file_path + '_header.json') as f:
        header_pos = json.load(f)
    return file_dict, header_pos


column = 'version'
value_to_check = '-'
conn_file_path = "./logs/tuesday/conn_labeled.log"
value_file_path = "./logs/ssl.log"
param_to_check = 'proto'

################ getting file_dict_conn and header_pos_conn
parsed_conn_file_path = './logs/tuesday/parsed/conn_labeled'
from os.path import exists
if not(exists(parsed_conn_file_path + '_dict.json') and exists(parsed_conn_file_path + '_header.json')):
    file_dict_conn, header_pos_conn = get_file_dict(conn_file_path)
    print_file_dict_to_file(parsed_conn_file_path, file_dict_conn, header_pos_conn)
else:
    file_dict_conn, header_pos_conn = read_file_dict_from_file(parsed_conn_file_path)

################ prendo tutti i valori usati di conn_state
'''
values = set([v.replace('\t', '') for v in get_all_values_of_columns(['conn_state'], file_dict_conn, header_pos_conn)])
all_values = set(['S0','S1','SF','REJ','S2','S3','RSTO','RSTR','RSTOS0','RSTRH','SH','SHR','OTH'])
print(all_values.difference(values))

'''
################ discretizzazione
import numpy as np
import matplotlib.pyplot as plt

attributes_to_digitize = {
    'duration': 10,
    'orig_bytes': 10,
    'resp_bytes': 10,
    'missed_bytes': 10,
    'orig_pkts': 10,
    'orig_ip_bytes': 10,
    'resp_pkts': 10,
    'resp_ip_bytes': 10,
}

#define function to calculate equal-frequency bins 
def equalObs(x, nbin):
    nlen = len(x)
    return np.interp(np.linspace(0, nlen, nbin + 1),
                     np.arange(nlen),
                     np.sort(x))

# getting max value for each attribute to digitize
for k, v in attributes_to_digitize.items():
    print('\n\n', k)
    arr_to_adjust = get_all_values_of_columns([k], file_dict_conn, header_pos_conn)
    data = [float(value.replace('\t', '')) for value in arr_to_adjust if value != '-\t']

    # showing equal-width
    n, bins, patches = plt.hist(data, edgecolor='black')
    plt.title(label=f'{k} - equal-width', fontsize=10)
    plt.show()

    print(bins)
    print(n)

    # showing equal-height
    n, bins, patches = plt.hist(data, equalObs(data, v), edgecolor='black')
    plt.title(label=f'{k} - equal-height | N = {v}', fontsize=10)
    plt.show()

    print(bins)
    print(n)

#file_dict_value, header_pos = get_file_dict(value_file_path)
#corr_found, corr_not_found, val_found = find_correlations_conn_column(file_dict_conn, header_pos_conn, file_dict_value, column, value_to_check)
#print(val_found)
#print_list_to_file(f"outputs/correlations_between_files_{column}/", f"corr_found_{value_to_check}.txt", corr_found)
#print_list_to_file(f"outputs/correlations_between_files_{column}/", f"corr_not_found_{value_to_check}.txt", corr_not_found)

#n = 10
#res = get_n_values_of_columns(['history', 'orig_pkts', 'resp_pkts'], n, file_dict_conn, header_pos_conn)
#for r in res:
 #   print(r)
'''

# applico le label agli event nei file
'''
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
apply_label_to_events_in_file(conn_file_path, "./logs/tuesday/conn_labeled.log", header_pos_conn, constraint_to_label)
'''

################### controllo che nello stesso trace sono presenti le stesse label
'''
print(header_pos_conn)
for trace, events in file_dict_conn.items():
    print(trace)
    for event in events:
        print(event)
    exit(0)
'''
'''
with open("./logs/tuesday/conn.log") as f:
    for line in f:
        with open("./logs/tuesday/merda.log", 'w') as f2:
            f2.write(line.replace('\n', '') + '\tlabel')
            exit(0)
'''
'''
same_label = []
diff_label = []
for trace, events in file_dict_conn.items():
    prev_label = events[0][header_pos_conn['label']]
    for event in events:
        new_label = event[header_pos_conn['label']]
        if new_label != prev_label:
            diff_label.append(trace)
            break
        else:
            prev_label = new_label
    else:
        same_label.append(trace)

print_list_to_file("output/", "traces_with_same_label.csv", same_label)
print_list_to_file("output/", "traces_with_diff_label.csv", diff_label)
'''

################### trovo il primo pacchetto con questo ip
'''
ip_da_trovare = ['172.16.0.1', '192.168.10.50']
with open(conn_file_path) as f:
    with open('output/ip_trovati.tsv', 'w') as f_out:
        for line in f:
            splitted = line.split('\t')
            orig = splitted[header_pos_conn['id.orig_h']]
            resp = splitted[header_pos_conn['id.resp_h']]
            if orig == ip_da_trovare[0] and resp == ip_da_trovare[1]:
                f_out.write(line)
'''

'''
header = ['history', 'orig_pkts', 'resp_pkts']
res_l = get_n_combinations_of_values_of_columns(header, file_dict_conn, header_pos_conn)
res_l.sort()
header.append('n_ricorrenze')
for res in res_l:
    for i, r in enumerate(res):
        res[i] = str(r)

res_l = [','.join(res) for res in res_l]
res_l.insert(0, ", ".join(header))
print_list_to_file("output/", "combinations_history_orig_pkts_resp_pkts.csv", res_l)
'''

'''
header = ['history']
res_history = get_n_combinations_of_values_of_columns(header, file_dict_conn, header_pos_conn)
res_history.sort(key = lambda row: (row[1]), reverse=True)
header.append('n_ricorrenze')
for res in res_history:
    for i, r in enumerate(res):
        res[i] = str(r)
res_history = [','.join(res) for res in res_history]
res_history.insert(0, ','.join(header))
#print_list_to_file("output/", "combinations_history_frequency.csv", res_history)


header = ['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto']
res_l = get_n_combinations_of_values_of_columns(header, file_dict_conn, header_pos_conn)
res_l = [" ".join(res[0:-1]) + ',' + str(res[-1]) for res in res_l]
res_l.sort()
print_list_to_file("output/", "combinations_conn_proto_frequency.csv", res_l)
'''

############### combinazioni di header nel file
'''
header = ['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto']
occ_dic = get_number_of_occurrencies_of_cols_from_file(conn_file_path, header)
occ_l = [[k, v] for k, v in occ_dic.items()]
occ_l.sort(key=lambda row: row[-1], reverse=True)
occ_copy = occ_l
occ_l = ['\t'.join([row[0], str(row[1])]) for row in occ_l]
print_list_to_file("output/", "combinations_conn_proto_frequency.tsv", occ_l)
'''

############### raggruppo le righe e creo la tabella con ts, durata e history
'''
header = ['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto', 'ts', 'duration', 'history']
res_l = list(get_all_values_of_columns(header, file_dict_conn, header_pos_conn))
res_l.sort(key = lambda row: (row[0], row[1], row[2], row[3], row[4]), reverse=True)
res_l = [res[:-1] for res in res_l]
res_l.insert(0, "\t".join(header))
print_list_to_file("output/", "combinazioni_raggruppamenti_delle_righe_ts_durata_history.tsv", res_l)
'''

############## raggruppo l'id con ts, duration e history
'''
id_list = ['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',]
cols = ['ts', 'duration', 'history']
out_l = get_values_of_columns(id_list, cols, file_dict_conn, header_pos_conn)
print('finito presi i valori')
out_l.sort()
print('finito sorting')

print_list_to_file("output/", "combinazioni_raggruppamenti_delle_righe_ts_durata_history.tsv", out_l)
new_out_l = []
for i in tqdm.tqdm(range(len(out_l) - 1)):
    new_out_l.append(out_l[i])
    if out_l[i].split('\t')[0] != out_l[i + 1].split('\t')[0]:
        new_out_l.append('')
print('finito mettere gli spazi')
print_list_to_file("output/", "combinazioni_raggruppamenti_delle_righe_ts_durata_history_separati_da_righe.tsv", new_out_l)
'''

############### Stampo delle history di esempio sulla console
'''
id_list = ['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',]
cols = ['ts', 'duration', 'history']
out_l = get_values_of_columns(id_list, cols, file_dict_conn, header_pos_conn)
n_history = 4
rand_indexes = [int(random() * len(out_l)) for _ in range(4)]
rh = RowHistory()
for i in rand_indexes:
    history = out_l[i].split('\t')[-1]
    print(out_l[i] + ":")
    for p in rh.get_history_with_values(history):
        print(p)
    print('\n')
'''

############### trova la cardinalità di tutte le righe con i valori di header
'''
header = ['history', 'orig_pkts', 'resp_pkts']
occ_dic = get_number_of_occurrencies_of_cols_from_file(conn_file_path, header)
occ_l = [[k, v] for k, v in occ_dic.items()]
occ_l.sort(key=lambda row: row[-1], reverse=True)
occ_copy = occ_l
occ_l = ['\t'.join([row[0], str(row[1])]) for row in occ_l]
print_list_to_file("output/", "combinations_history_pkts_cardinality.tsv", occ_l)

values = [occ[0] for occ in occ_copy]
print_list_to_file("output/", "combinations_history_pkts_values.tsv", values)


############ trovo la cardinalità delle cardinalità

card_dict = {}
for occ in occ_copy:
    key = occ[-1]
    if key in card_dict:
        card_dict[key] += 1
    else:
        card_dict[key] = 1

card_of_card_l = [[k, v] for k, v in card_dict.items()]
#card_of_card_l.sort(key=lambda row: row[-1], reverse=True)
card_of_card_l = ['\t'.join([str(row[0]), str(row[1])]) for row in card_of_card_l]
print_list_to_file("output/", "combinations_cardinality_frequency.tsv", card_of_card_l)
'''

#res = get_all_values_of_columns(['curve'], file_dict_conn, header_pos_conn)
#for r in res:
#   print(r)

#print(count_ric_val_col('./logs/ocsp.log', 'id'))

#for h in header_pos_conn:
#    print(h)

#param_dict = check_param(param_to_check, file_dict_conn, header_pos_conn)
#print_checked_param(param_to_check, param_dict)



############## Ripulisce tutti i file dagli #
'''
clean_files([
    'logs/monday/conn.log',
    'logs/monday/dce_rpc.log',
    'logs/monday/dns.log',
    'logs/monday/dpd.log',
    'logs/monday/files.log',
    'logs/monday/ftp.log',
    'logs/monday/http.log',
    'logs/monday/kerberos.log',
    'logs/monday/ntlm.log',
    'logs/monday/ntp.log',
    'logs/monday/ocsp.log',
    'logs/monday/packet_filter.log',
    'logs/monday/pe.log',
    'logs/monday/smb_files.log',
    'logs/monday/smb_mapping.log',
    'logs/monday/ssh.log',
    'logs/monday/ssl.log',
    'logs/monday/weird.log',
    'logs/monday/x509.log',

    'logs/tuesday/conn.log',
    'logs/tuesday/dce_rpc.log',
    'logs/tuesday/dns.log',
    'logs/tuesday/dpd.log',
    'logs/tuesday/files.log',
    'logs/tuesday/ftp.log',
    'logs/tuesday/http.log',
    'logs/tuesday/kerberos.log',
    'logs/tuesday/ntlm.log',
    'logs/tuesday/ntp.log',
    'logs/tuesday/ocsp.log',
    'logs/tuesday/packet_filter.log',
    'logs/tuesday/pe.log',
    'logs/tuesday/smb_files.log',
    'logs/tuesday/smb_mapping.log',
    'logs/tuesday/ssh.log',
    'logs/tuesday/ssl.log',
    'logs/tuesday/weird.log',
    'logs/tuesday/x509.log',

    'logs/wednesday/conn.log',
    'logs/wednesday/dce_rpc.log',
    'logs/wednesday/dns.log',
    'logs/wednesday/dpd.log',
    'logs/wednesday/files.log',
    'logs/wednesday/ftp.log',
    'logs/wednesday/http.log',
    'logs/wednesday/kerberos.log',
    'logs/wednesday/ntlm.log',
    'logs/wednesday/ntp.log',
    'logs/wednesday/ocsp.log',
    'logs/wednesday/packet_filter.log',
    'logs/wednesday/pe.log',
    'logs/wednesday/smb_files.log',
    'logs/wednesday/smb_mapping.log',
    'logs/wednesday/ssh.log',
    'logs/wednesday/ssl.log',
    'logs/wednesday/weird.log',
    'logs/wednesday/x509.log',

    'logs/thursday/conn.log',
    'logs/thursday/dce_rpc.log',
    'logs/thursday/dns.log',
    'logs/thursday/dpd.log',
    'logs/thursday/files.log',
    'logs/thursday/ftp.log',
    'logs/thursday/http.log',
    'logs/thursday/kerberos.log',
    'logs/thursday/ntlm.log',
    'logs/thursday/ntp.log',
    'logs/thursday/ocsp.log',
    'logs/thursday/packet_filter.log',
    'logs/thursday/pe.log',
    'logs/thursday/smb_files.log',
    'logs/thursday/smb_mapping.log',
    'logs/thursday/ssh.log',
    'logs/thursday/ssl.log',
    'logs/thursday/weird.log',
    'logs/thursday/x509.log',
    
    'logs/friday/conn.log',
    'logs/friday/dce_rpc.log',
    'logs/friday/dns.log',
    'logs/friday/dpd.log',
    'logs/friday/files.log',
    'logs/friday/ftp.log',
    'logs/friday/http.log',
    'logs/friday/kerberos.log',
    'logs/friday/ntlm.log',
    'logs/friday/ntp.log',
    'logs/friday/ocsp.log',
    'logs/friday/packet_filter.log',
    'logs/friday/pe.log',
    'logs/friday/smb_files.log',
    'logs/friday/smb_mapping.log',
    'logs/friday/ssh.log',
    'logs/friday/ssl.log',
    'logs/friday/weird.log',
    'logs/friday/x509.log',
    ])
'''




############# raggruppa i log di ogni file per tutti i giorni
'''
master_folder = 'logs/'
input_folders = [
    'monday/',
    'tuesday/',
    'wednesday/',
    'thursday/',
    'friday/',
]
output_folder = 'total_logs/'

files = [
    'conn.log',
    'dce_rpc.log',
    'dns.log',
    'dpd.log',
    'files.log',
    'ftp.log',
    'http.log',
    'kerberos.log',
    'ntlm.log',
    'ntp.log',
    'ocsp.log',
    'packet_filter.log',
    'pe.log',
    'smb_files.log',
    'smb_mapping.log',
    'ssh.log',
    'ssl.log',
    'weird.log',
    'x509.log',
]

for file in files:
    input_files_path = [master_folder + folder + file for folder in input_folders]
    copy_contents_of_files_into_another_file(input_files_path, master_folder + output_folder + file)
'''

