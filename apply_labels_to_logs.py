from datetime import datetime
import csv
import tqdm

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
    print('applying labels...')
    n_lines = 0
    with open(input_files_path, 'r') as f_in:
        n_lines = len(f_in.readlines()) - 1

    labels_applied = []
    matched_attacker = []
    matched_attacked = []
    both = []
    with open(output_file_path, 'w') as f_out:
        with open(input_files_path, 'r') as f_in:
            line = next(f_in)
            line = line.replace('\n', '')
            f_out.write(line + '\tlabel\n')
            for _ in tqdm.tqdm(range(n_lines)):
                found = False # the ips correspond
                line = next(f_in)
                line = line.replace('\n', '')
                splitted = line.split('\t')
                ts = splitted[header_pos['ts']]
                orig_ip = splitted[header_pos['id.orig_h']]
                resp_ip = splitted[header_pos['id.resp_h']]
                for constraints in constraint_to_label:
                    label = constraints['label']
                    attacker = constraints['ip_attacker']
                    attacked = constraints['ip_attacked']
                    if (orig_ip in attacker):
                        matched_attacker.append(orig_ip)
                    if (resp_ip in attacked):
                        matched_attacked.append(resp_ip)
                    if (orig_ip in attacker and resp_ip in attacked):
                        both.append((orig_ip, resp_ip))
                    if ((orig_ip in attacker or 'everyone' in attacker) and
                        (resp_ip in attacked or 'everyone' in attacked)):
                        found = True
                        if (float(constraints['lower_bound']) <= float(ts) <= float(constraints['upper_bound'])):
                            line += '\t' + label
                            labels_applied.append(label)
                            f_out.write(f'{line}\n')
                            break
                else: # no break
                    if not found:
                        line += '\t' + 'Normal'
                        f_out.write(f'{line}\n')
                    else:
                        found = False

    from collections import Counter
    print('attacker:')
    print('\t', set(matched_attacker))
    print('\t', len(matched_attacker))
    print('\t', Counter(matched_attacker))
    print('attacked:')
    print('\t', set(matched_attacked))
    print('\t', len(matched_attacked))
    print('\t', Counter(matched_attacked))
    print('both:')
    print('\t', set(both))
    print('\t', len(both))
    print('\t', Counter(both))
    print('labels applied:')
    print('\t', set(labels_applied))
    print('\t', len(labels_applied))
    print('\t', Counter(labels_applied))


################ getting file_dict_conn and header_pos_conn

def get_header_pos_conn(conn_file_path):
    with open(conn_file_path, 'r') as f_log:
        csvr = csv.reader(f_log, delimiter="\t")
        header = next(csvr)
        header_pos = {h: i for i, h in enumerate(header)}
    return header_pos

def conv_time(day: int, h: int):
    h_5 = h + 5
    return f"{day + (1 if h_5 > 24 else 0)} {h_5 % 24}"

# applico le label agli event nei file
import time
import datetime

constraint_to_label_monday = []







constraint_to_label_tuesday = [
    # Morning
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(4, 9)}:20:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(4, 10)}:20:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(4, 14)}:00:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(4, 15)}:00:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
]







constraint_to_label_wednesday = [
    # Morning
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 9)}:47:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 10)}:10:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 10)}:14:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 10)}:35:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 10)}:43:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 11)}:00:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 11)}:10:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 11)}:23:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 15)}:12:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(5, 15)}:32:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
]







constraint_to_label_thursday = [
    # Morning
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 9)}:20:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 10)}:00:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 10)}:15:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 10)}:35:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 10)}:40:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 10)}:42:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },

    # Afternoon
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 14)}:19:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 14)}:35:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '192.168.10.8',
            },
        'ip_attacked': {
            '205.174.165.73',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 14)}:53:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 15)}:00:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '192.168.10.25',
            },
        'ip_attacked': {
            '205.174.165.73',
            },
        'label': 'Anomaly',
    },

    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 15)}:04:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 15)}:45:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '192.168.10.8',
            },
        'ip_attacked': {
            '205.174.165.73',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 15)}:04:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(6, 15)}:45:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '192.168.10.8',
            },
        'ip_attacked': {
            'everyone',
            },
        'label': 'Anomaly',
    },
]






constraint_to_label_friday = [
    # Morning
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 10)}:02:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 11)}:02:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '192.168.10.15',
            '192.168.10.9',
            '192.168.10.14',
            '192.168.10.5',
            '192.168.10.8',
            },
        'ip_attacked': {
            '205.174.165.73',
            },
        'label': 'Anomaly',
    },
    # Afternoon
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 13)}:55:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:24:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:33:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:33:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:35:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:35:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },



    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:51:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:53:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:54:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:56:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:57:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 14)}:59:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:00:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:02:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:03:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:05:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:06:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:07:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:08:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:10:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:11:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:12:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:13:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:15:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:16:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:18:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:19:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:21:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:22:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:24:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:25:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:25:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:26:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:27:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:28:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:29:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
    {
        'lower_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 15)}:56:00", '%Y-%m-%d %H:%M:%S').timetuple()),
        'upper_bound': time.mktime(datetime.datetime.strptime(f"2017-07-{conv_time(7, 16)}:16:59", '%Y-%m-%d %H:%M:%S').timetuple()),
        'ip_attacker': {
            '172.16.0.1',
            },
        'ip_attacked': {
            '192.168.10.50',
            },
        'label': 'Anomaly',
    },
]


import sys
import os

if __name__ == '__main__':
    day = sys.argv[1]
    conn_file_path = sys.argv[2]

    constraint_dict = {
        'monday': constraint_to_label_monday,
        'tuesday': constraint_to_label_tuesday,
        'wednesday': constraint_to_label_wednesday,
        'thursday': constraint_to_label_thursday,
        'friday': constraint_to_label_friday,
    }

    if day not in constraint_dict:
        print('Error: day not valid, these are the valid days:\n- monday,\n- tuesday,\n- wednesday,\n- thursday,\n- friday\n')
    else:
        constraint_to_apply = constraint_dict[day]
        if os.path.exists(conn_file_path):
            header_pos_conn = get_header_pos_conn(conn_file_path)
            apply_label_to_events_in_file(conn_file_path, conn_file_path.replace(".log", "_labeled.log"), header_pos_conn, constraint_to_apply)
        else:
            print('Error: file: "' + conn_file_path + '" does not exists')

