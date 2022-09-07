from datetime import datetime
import csv
from email import header
from random import random
import tqdm

class RowHistory:
    '''
    Class that manages the history of a single row, takes the string history
    and according to its characters sets single fields of this object to their value
    :param history: history to be converted
    :type history: str
    :param orig_syn: Origin sent this number of packets with a SYN bit set w/o the ACK bit set
    :type orig_syn: int
    :param orig_fin: Origin sent this number of packets with a FIN bit set
    :type orig_fin: int
    :param orig_syn_ack: Origin sent this number of packets with a SYN with the ACK bit set
    :type orig_syn_ack: int
    :param orig_rest: Origin sent this number of packets with a RST bit set
    :type orig_rest: int
    :param resp_syn: Responder sent this number of packets with a SYN bit set w/o the ACK bit set
    :type resp_syn: int
    :param resp_fin: Responder sent this number of packets with a FIN bit set 
    :type resp_fin: int
    :param resp_syn_ack: Responder sent this number of packets with a SYN with the ACK bit set
    :type resp_syn_ack: int
    :param resp_rest: Responder sent this number of packets with a RST bit set
    :type resp_rest: int
    :param orig_ack: Origin sent a packet with ACK bit set
    :type orig_ack: bool
    :param orig_payload: Origin sent a payload
    :type orig_payload: bool
    :param orig_inconsistent: Origin packet was inconsistent (e.g. FIN+RST bits set)
    :type orig_inconsistent: bool
    :param orig_multi_flag: Origin sent a multi-flag packet (SYN+FIN or SYN+RST bits set)
    :type orig_multi_flag: bool
    :param resp_ack: Responder sent a packet with ACK bit set
    :type resp_ack: bool
    :param resp_payload: Responder sent a payload
    :type resp_payload: bool
    :param resp_inconsistent: Responder packet was inconsistent (e.g. FIN+RST bits set)
    :type resp_inconsistent: bool
    :param resp_multi_flag: Responder sent a multi-flag packet (SYN+FIN or SYN+RST bits set)
    :type resp_multi_flag: bool
    :param orig_bad_checksum: Origin sent this number of packets with a bad checksum
    :type orig_bad_checksum: int 
    :param orig_content_gap: Origin sent this number of packets with content gap
    :type orig_content_gap: int 
    :param orig_retransmitted_payload: Origin retransmitted this number of packets with payload
    :type orig_retransmitted_payload: int 
    :param orig_zero_window: Origin sent this number of packet with zero window
    :type orig_zero_window: int 
    :param resp_bad_checksum: Responder sent this number of packets with a bad checksum
    :type resp_bad_checksum: int 
    :param resp_content_gap: Responder sent this number of packets with content gap
    :type resp_content_gap: int 
    :param resp_retransmitted_payload: Responder retransmitted this number of packets with payload
    :type resp_retransmitted_payload: int 
    :param resp_zero_window: Responder sent this number of packet with zero window
    :type resp_zero_window: int 
    :param conn_dir_flipped: Connection direction was flipped by Zeek's heuristic
    :type conn_dir_flipped: bool
    '''

    def __init__(self, history: str=None) -> None:
        self.__history = history if history is not None else ''

        # S, F, H, R
        self.__orig_syn                   = 0
        self.__orig_fin                   = 0
        self.__orig_syn_ack               = 0
        self.__orig_rest                  = 0

        # s, f, h, r
        self.__resp_syn                   = 0
        self.__resp_fin                   = 0
        self.__resp_syn_ack               = 0
        self.__resp_rest                  = 0
        
        # A, D, I, Q
        self.__orig_ack                   = False
        self.__orig_payload               = False
        self.__orig_inconsistent          = False
        self.__orig_multi_flag            = False

        # a, d, i, q
        self.__resp_ack                   = False
        self.__resp_payload               = False
        self.__resp_inconsistent          = False
        self.__resp_multi_flag            = False
        
        # C, G, T, W
        self.__orig_bad_checksum          = 0
        self.__orig_content_gap           = 0
        self.__orig_retransmitted_payload = 0
        self.__orig_zero_window           = 0

        # c, g, t, w
        self.__resp_bad_checksum          = 0
        self.__resp_content_gap           = 0
        self.__resp_retransmitted_payload = 0
        self.__resp_zero_window           = 0

        # ^
        self.__conn_dir_flipped           = False
        
        self.analyze_history()

    def analyze_history(self, history: str=None) -> None:
        """Based on the field history, this analyze the history string and changes
        all the fields of this object. If given a history, this will be analyzed and set
        as this object history

        :param history: the history to be analyzed, defaults to None
        :type history: str, optional
        """

        if history is not None:
            self.__history = history

        for c in self.__history:
            if c == 'S': self.__orig_syn += 1
            elif c == 'F': self.__orig_fin += 1
            elif c == 'H': self.__orig_syn_ack += 1
            elif c == 'R': self.__orig_rest += 1
            
            elif c == 's': self.__resp_syn += 1
            elif c == 'f': self.__resp_fin += 1
            elif c == 'h': self.__resp_syn_ack += 1
            elif c == 'r': self.__resp_rest += 1

            elif c == 'A': self.__orig_ack = True
            elif c == 'D': self.__orig_payload = True
            elif c == 'I': self.__orig_inconsistent = True
            elif c == 'Q': self.__orig_multi_flag = True

            elif c == 'a': self.__resp_ack = True
            elif c == 'd': self.__resp_payload = True
            elif c == 'i': self.__resp_inconsistent = True
            elif c == 'q': self.__resp_multi_flag = True

            elif c == 'C': self.__orig_bad_checksum += 1
            elif c == 'G': self.__orig_content_gap += 1
            elif c == 'T': self.__orig_retransmitted_payload += 1
            elif c == 'W': self.__orig_zero_window += 1

            elif c == 'c': self.__resp_bad_checksum += 1
            elif c == 'g': self.__resp_content_gap += 1
            elif c == 't': self.__resp_retransmitted_payload += 1
            elif c == 'w': self.__resp_zero_window += 1

            elif c == '^': self.__conn_dir_flipped = True

    def get_history_with_values(self, history: str=None) -> list:
        """Returns a list of the tuples where the first element of the tuple
        is the character red, the second is the value itself.__ If a history string is given, 
        the list is relative to that history and this object's history value is changed

        :param history: history to be transformed, defaults to None
        :type history: str, optional
        :return: list of the tuples of the history
        :rtype: list
        """        

        if history is not None:
            self.analyze_history(history)
        
        return [self.__history,
            ('S', self.__orig_syn),
            ('F', self.__orig_fin),
            ('H', self.__orig_syn_ack),
            ('R', self.__orig_rest),

            ('s', self.__resp_syn),
            ('f', self.__resp_fin),
            ('h', self.__resp_syn_ack),
            ('r', self.__resp_rest),

            ('A', self.__orig_ack),
            ('D', self.__orig_payload),
            ('I', self.__orig_inconsistent),
            ('Q', self.__orig_multi_flag),

            ('a', self.__resp_ack),
            ('d', self.__resp_payload),
            ('i', self.__resp_inconsistent),
            ('q', self.__resp_multi_flag),

            ('C', self.__orig_bad_checksum),
            ('G', self.__orig_content_gap),
            ('T', self.__orig_retransmitted_payload),
            ('W', self.__orig_zero_window),

            ('c', self.__resp_bad_checksum),
            ('g', self.__resp_content_gap),
            ('t', self.__resp_retransmitted_payload),
            ('w', self.__resp_zero_window),

            ('^', self.__conn_dir_flipped),
        ]

    def get_history_with_description(self, history: str=None) -> list:
        """Returns a list where for each element, there is a string describing the letter red
        at that position. If a history string is given, the list is relative to that history and
        this object's history value is changed

        :param history: history to be transformed, defaults to None
        :type history: str, optional
        :return: list of the description of each letter
        :rtype: list
        """        
        """Returns a list where for each element, there is a string describing the letter red
        at that position

        :return: list of the description of each letter
        :rtype: list
        """
        if history is not None:
            self.analyze_history(history)

        out_list = [] # lista delle stringhe corrispondenti alle fasi della history
        for i, c in enumerate(self.__history):
            if c == 'S': out_list.append(f'{i + 1}. Origin sent a packet with a SYN bit set w/o the ACK bit set')
            elif c == 'F': out_list.append(f'{i + 1}. Origin sent a packet with a FIN bit set')
            elif c == 'H': out_list.append(f'{i + 1}. Origin sent a packet with a SYN with the ACK bit set')
            elif c == 'R': out_list.append(f'{i + 1}. Origin sent a packet with a RST bit set')
            
            elif c == 's': out_list.append(f'{i + 1}. Responder sent a packet with a SYN bit set w/o the ACK bit set')
            elif c == 'f': out_list.append(f'{i + 1}. Responder sent a packet with a FIN bit set ')
            elif c == 'h': out_list.append(f'{i + 1}. Responder sent a packet with a SYN with the ACK bit set')
            elif c == 'r': out_list.append(f'{i + 1}. Responder sent a packet with a RST bit set')

            elif c == 'A': out_list.append(f'{i + 1}. Origin sent a packet with ACK bit set')
            elif c == 'D': out_list.append(f'{i + 1}. Origin sent a payload')
            elif c == 'I': out_list.append(f'{i + 1}. Origin packet was inconsistent (e.g. FIN+RST bits set)')
            elif c == 'Q': out_list.append(f'{i + 1}. Origin sent a multi-flag packet (SYN+FIN or SYN+RST bits set)')

            elif c == 'a': out_list.append(f'{i + 1}. Responder sent a packet with ACK bit set')
            elif c == 'd': out_list.append(f'{i + 1}. Responder sent a payload')
            elif c == 'i': out_list.append(f'{i + 1}. Responder packet was inconsistent (e.g. FIN+RST bits set)')
            elif c == 'q': out_list.append(f'{i + 1}. Responder sent a multi-flag packet (SYN+FIN or SYN+RST bits set)')

            elif c == 'C': out_list.append(f'{i + 1}. Origin sent a packet with a bad checksum')
            elif c == 'G': out_list.append(f'{i + 1}. Origin sent a packet with content gap')
            elif c == 'T': out_list.append(f'{i + 1}. Origin retransmitted a packet with payload')
            elif c == 'W': out_list.append(f'{i + 1}. Origin sent a packet with zero window')

            elif c == 'c': out_list.append(f'{i + 1}. Responder sent a packet with a bad checksum')
            elif c == 'g': out_list.append(f'{i + 1}. Responder sent a packet with content gap')
            elif c == 't': out_list.append(f'{i + 1}. Responder retransmitted a packet with payload')
            elif c == 'w': out_list.append(f'{i + 1}. Responder sent a packet with zero window')

            elif c == '^': out_list.append(f"{i + 1}. Connection direction was flipped by Zeek's heuristic")

        return out_list


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

column = 'version'
value_to_check = '-'
conn_file_path = "./logs/tuesday/conn.log"
value_file_path = "./logs/ssl.log"
param_to_check = 'proto'
file_dict_conn, header_pos_conn = get_file_dict(conn_file_path)
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
res_history.insert(0, ", ".join(header))
print_list_to_file("output/", "combinations_history_frequency.csv", res_history)


header = ['id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p']
res_l = get_n_combinations_of_values_of_columns(header, file_dict_conn, header_pos_conn)
res_l = [" ".join(res[0:-1]) + ", " + str(res[-1]) for res in res_l]
res_l.sort()
print_list_to_file("output/", "combinations_conn_proto_frequency.csv", res_l)
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
    h_lower = out_l[i].split('\t')[-1].lower()
    if 'c' in h_lower or 'g' in h_lower or 't' in h_lower or 'w' in h_lower:
        new_out_l.append(out_l[i])
        if out_l[i].split('\t')[0] != out_l[i + 1].split('\t')[0]:
            new_out_l.append('')
print('finito mettere gli spazi')
print_list_to_file("output/", "combinazioni_raggruppamenti_delle_righe_ts_durata_history_separati_da_righe.tsv", new_out_l)
'''

############### Stampo delle history di esempio sulla console
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
'''

############ trovo la cardinalità delle cardinalità
'''
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