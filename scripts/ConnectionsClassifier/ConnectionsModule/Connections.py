import json
from dataclasses import dataclass
from enum import Enum, auto
from DiscretizerModule.Discretizer import Discretizer

class CONN_STATE(Enum):
    """
    Describes the state that a Connection can have
    #. S0: Connection attempt seen, no reply.
    #. S1: Connection established, not terminated.
    #. SF: Normal establishment and termination. Note that this is the same symbol as for state S1. You can tell the two apart because for S1 there will not be any byte counts in the summary, while for SF there will be.
    #. REJ: Connection attempt rejected.
    #. S2: Connection established and close attempt by originator seen (but no reply from responder).
    #. S3: Connection established and close attempt by responder seen (but no reply from originator).
    #. RSTO: Connection established, originator aborted (sent a RST).
    #. RSTR: Responder sent a RST.
    #. RSTOS0: Originator sent a SYN followed by a RST, we never saw a SYN-ACK from the responder.
    #. RSTRH: Responder sent a SYN ACK followed by a RST, we never saw a SYN from the (purported) originator.
    #. SH: Originator sent a SYN followed by a FIN, we never saw a SYN ACK from the responder (hence the connection was “half” open).
    #. SHR: Responder sent a SYN ACK followed by a FIN, we never saw a SYN from the originator.
    #. OTH: No SYN seen, just midstream traffic (one example of this is a “partial connection” that was not later closed).
    """    
    S0 = auto()
    S1 = auto()
    SF = auto()
    REJ = auto()
    S2 = auto()
    S3 = auto()
    RSTO = auto()
    RSTR = auto()
    RSTOS0 = auto()
    RSTRH = auto()
    SH = auto()
    SHR = auto()
    OTH = auto()

    def __str__(self):
        return f'{self.name(self.value)}'

class EventHistory:
    '''
    Class that manages the history of a single event, takes the string history
    and according to its characters sets single fields of this object to their value

    :param __history: history to be converted
    :type __history: str
    :param __orig_syn: Origin sent this number of packets with a SYN bit set w/o the ACK bit set
    :type __orig_syn: float
    :param __orig_fin: Origin sent this number of packets with a FIN bit set
    :type __orig_fin: float
    :param __orig_syn_ack: Origin sent this number of packets with a SYN with the ACK bit set
    :type __orig_syn_ack: float
    :param __orig_rest: Origin sent this number of packets with a RST bit set
    :type __orig_rest: float
    :param __resp_syn: Responder sent this number of packets with a SYN bit set w/o the ACK bit set
    :type __resp_syn: float
    :param __resp_fin: Responder sent this number of packets with a FIN bit set 
    :type __resp_fin: float
    :param __resp_syn_ack: Responder sent this number of packets with a SYN with the ACK bit set
    :type __resp_syn_ack: float
    :param __resp_rest: Responder sent this number of packets with a RST bit set
    :type __resp_rest: float
    :param __orig_ack: Origin sent a packet with ACK bit set
    :type __orig_ack: bool
    :param __orig_payload: Origin sent a payload
    :type __orig_payload: bool
    :param __orig_inconsistent: Origin packet was inconsistent (e.g. FIN+RST bits set)
    :type __orig_inconsistent: bool
    :param __orig_multi_flag: Origin sent a multi-flag packet (SYN+FIN or SYN+RST bits set)
    :type __orig_multi_flag: bool
    :param __resp_ack: Responder sent a packet with ACK bit set
    :type __resp_ack: bool
    :param __resp_payload: Responder sent a payload
    :type __resp_payload: bool
    :param __resp_inconsistent: Responder packet was inconsistent (e.g. FIN+RST bits set)
    :type __resp_inconsistent: bool
    :param __resp_multi_flag: Responder sent a multi-flag packet (SYN+FIN or SYN+RST bits set)
    :type __resp_multi_flag: bool
    :param __orig_bad_checksum: Origin sent this number of packets with a bad checksum
    :type __orig_bad_checksum: float 
    :param __orig_content_gap: Origin sent this number of packets with content gap
    :type __orig_content_gap: float 
    :param __orig_retransmitted_payload: Origin retransmitted this number of packets with payload
    :type __orig_retransmitted_payload: float 
    :param __orig_zero_window: Origin sent this number of packet with zero window
    :type __orig_zero_window: float 
    :param __resp_bad_checksum: Responder sent this number of packets with a bad checksum
    :type __resp_bad_checksum: float 
    :param __resp_content_gap: Responder sent this number of packets with content gap
    :type __resp_content_gap: float 
    :param __resp_retransmitted_payload: Responder retransmitted this number of packets with payload
    :type __resp_retransmitted_payload: float 
    :param __resp_zero_window: Responder sent this number of packet with zero window
    :type __resp_zero_window: float 
    :param __conn_dir_flipped: Event direction was flipped by Zeek's heuristic
    :type __conn_dir_flipped: bool

    :param disc_orig_syn: Discretizer of the relative attribute
    :type disc_orig_syn: Discretizer
    :param disc_orig_fin: Discretizer of the relative attribute
    :type disc_orig_fin: Discretizer
    :param disc_orig_syn_ack: Discretizer of the relative attribute
    :type disc_orig_syn_ack: Discretizer
    :param disc_orig_rst: Discretizer of the relative attribute
    :type disc_orig_rst: Discretizer
    :param disc_resp_syn: Discretizer of the relative attribute
    :type disc_resp_syn: Discretizer
    :param disc_resp_fin: Discretizer of the relative attribute
    :type disc_resp_fin: Discretizer
    :param disc_resp_syn_ack: Discretizer of the relative attribute
    :type disc_resp_syn_ack: Discretizer
    :param disc_resp_rst: Discretizer of the relative attribute
    :type disc_resp_rst: Discretizer
    :param disc_orig_bad_checksum: Discretizer of the relative attribute
    :type disc_orig_bad_checksum: Discretizer
    :param disc_orig_content_gap: Discretizer of the relative attribute
    :type disc_orig_content_gap: Discretizer
    :param disc_orig_retransmitted: Discretizer of the relative attribute
    :type disc_orig_retransmitted: Discretizer
    :param disc_orig_zero_window: Discretizer of the relative attribute
    :type disc_orig_zero_window: Discretizer
    :param disc_resp_bad_checksum: Discretizer of the relative attribute
    :type disc_resp_bad_checksum: Discretizer
    :param disc_resp_conten_gap: Discretizer of the relative attribute
    :type disc_resp_conten_gap: Discretizer
    :param disc_resp_retransmitted: Discretizer of the relative attribute
    :type disc_resp_retransmitted: Discretizer
    :param disc_resp_zero_window: Discretizer of the relative attribute
    :type disc_resp_zero_window: Discretizer
    '''

    # S, F, H, R Discretized
    disc_orig_syn: Discretizer = None
    disc_orig_fin: Discretizer = None
    disc_orig_syn_ack: Discretizer = None
    disc_orig_rst: Discretizer = None

    # s, f, h, r Discretized
    disc_resp_syn: Discretizer = None
    disc_resp_fin: Discretizer = None
    disc_resp_syn_ack: Discretizer = None
    disc_resp_rst: Discretizer = None

    # c, g, t, w Discretized
    disc_orig_bad_checksum: Discretizer = None
    disc_orig_content_gap: Discretizer = None
    disc_orig_retransmitted: Discretizer = None
    disc_orig_zero_window: Discretizer = None

    # C, G, T, W Discretized
    disc_resp_bad_checksum: Discretizer = None
    disc_resp_conten_gap: Discretizer = None
    disc_resp_retransmitted: Discretizer = None
    disc_resp_zero_window: Discretizer = None

    def __init__(self, history: str=None) -> None:
        """The constructor initialize the parameters required and if history is given,
        it analyze the string and assigns the relativa values to the fields

        :param history: string to be analyzed, defaults to None
        :type history: str, optional
        """
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

            elif c == '^': out_list.append(f"{i + 1}. Event direction was flipped by Zeek's heuristic")

        return out_list

    def to_json_obj(self) -> object:
        """
        converts this class object to an object that can be easily dumped in a json file

        :return: object that can be converted to a json file
        :rtype: object
        """
        return {
            'history': self.__history,
            'S': self.__orig_syn,
            'F': self.__orig_fin,
            'H': self.__orig_syn_ack,
            'R': self.__orig_rest,
            's': self.__resp_syn,
            'f': self.__resp_fin,
            'h': self.__resp_syn_ack,
            'r': self.__resp_rest,
            'A': self.__orig_ack,
            'D': self.__orig_payload,
            'I': self.__orig_inconsistent,
            'Q': self.__orig_multi_flag,
            'a': self.__resp_ack,
            'd': self.__resp_payload,
            'i': self.__resp_inconsistent,
            'q': self.__resp_multi_flag,
            'C': self.__orig_bad_checksum,
            'G': self.__orig_content_gap,
            'T': self.__orig_retransmitted_payload,
            'W': self.__orig_zero_window,
            'c': self.__resp_bad_checksum,
            'g': self.__resp_content_gap,
            't': self.__resp_retransmitted_payload,
            'w': self.__resp_zero_window,
            '^': self.__conn_dir_flipped,
        }

class Event:
    '''
    Class of a single event registered

    This class contains all of the data that are going to be used
    to classify this event

    :param ts: timestamp of this event
    :type ts: str
    :param service: An identification of an application protocol being sent over the event.
    :type service: str
    :param state: state of the event
    :type state: str
    :param duration: How long the event lasted. For 3-way or 4-way event tear-downs, this will not include the final ACK.
    :type duration: float
    :param orig_bytes: number of bytes sent by the origin
    :type orig_bytes: float
    :param resp_bytes: number of bytes sent by the responder
    :type resp_bytes: float
    :param conn_state: state of this event
    :type conn_state: str
    :param missed_bytes: bytes missed during this event
    :type missed_bytes: float
    :param history: state history of this event.
    :type history: EventHistory
    :param orig_pkts: Number of packets that the originator sent
    :type orig_pkts: float
    :param orig_ip_bytes: Number of IP level bytes that the originator sent (as seen on the wire, taken from the IP total_length header field
    :type orig_ip_bytes: float
    :param resp_pkts: Number of packets that the responder sent.
    :type resp_pkts: float
    :param resp_ip_bytes: Number of IP level bytes that the responder sent (as seen on the wire, taken from the IP total_length header field
    :type resp_ip_bytes: float
    
    :param disc_orig_bytes: Discretizer of the relative attribute
    :type disc_orig_bytes: Discretizer
    :param disc_resp_bytes: Discretizer of the relative attribute
    :type disc_resp_bytes: Discretizer
    :param disc_missed_bytes: Discretizer of the relative attribute
    :type disc_missed_bytes: Discretizer
    :param disc_orig_pkts: Discretizer of the relative attribute
    :type disc_orig_pkts: Discretizer
    :param disc_duration: Discretizer of the relative attribute
    :type disc_duration: Discretizer
    :param disc_orig_ip_bytes: Discretizer of the relative attribute
    :type disc_orig_ip_bytes: Discretizer
    :param disc_resp_pkts: Discretizer of the relative attribute
    :type disc_resp_pkts: Discretizer
    :param disc_resp_ip_bytes: Discretizer of the relative attribute
    :type disc_resp_ip_bytes: Discretizer
    '''
    disc_orig_bytes: Discretizer = None
    disc_resp_bytes: Discretizer = None
    disc_missed_bytes: Discretizer = None
    disc_orig_pkts: Discretizer = None
    disc_duration: Discretizer = None
    disc_orig_ip_bytes: Discretizer = None
    disc_resp_pkts: Discretizer = None
    disc_resp_ip_bytes: Discretizer = None

    def __init__(self, 
            ts: str,
            service: str,
            duration: float,
            orig_bytes: float,
            resp_bytes: float,
            conn_state: str,
            missed_bytes: float,
            history: EventHistory,
            orig_pkts: float,
            orig_ip_bytes: float,
            resp_pkts: float,
            resp_ip_bytes: float,
            label: str) -> None:    
        self.__ts = ts
        self.__service = service
        self.__duration = duration
        self.__orig_bytes = orig_bytes
        self.__resp_bytes = resp_bytes
        self.__conn_state = conn_state
        self.__missed_bytes = missed_bytes
        self.__history = history
        self.__orig_pkts = orig_pkts
        self.__orig_ip_bytes = orig_ip_bytes
        self.__resp_pkts = resp_pkts
        self.__resp_ip_bytes = resp_ip_bytes
        self.__label = label

    def to_json_obj(self) -> object:
        """
        converts this class object to an object that can be easily dumped in a json file

        :return: object that can be converted to a json file
        :rtype: object
        """
        return {
            'ts': self.__ts,
            'services': self.__service,
            'duration': self.__duration,
            'orig_bytes': self.__orig_bytes,
            'resp_bytes': self.__resp_bytes,
            'conn_state': self.__conn_state,
            'missed_bytes': self.__missed_bytes,
            'history': self.__history,
            'orig_pkts': self.__orig_pkts,
            'orig_ip_bytes': self.__orig_ip_bytes,
            'resp_pkts': self.__resp_pkts,
            'resp_ip_bytes': self.__resp_ip_bytes,
            'label': self.__label,
        }
    
    def get_ts(self) -> str:
        """Getter of ts

        :return: the value of ts
        :rtype: str
        """
        return self.__ts

    def get_service(self) -> str:
        """Getter of service

        :return: the value of service
        :rtype: str
        """
        return self.__service

    def get_duration(self) -> float:
        """Getter of duration

        :return: the value of duration
        :rtype: float
        """
        return self.__duration

    def get_orig_bytes(self) -> float:
        """Getter of orig_bytes

        :return: the value of orig_bytes
        :rtype: float
        """
        return self.__orig_bytes

    def get_resp_bytes(self) -> float:
        """Getter of resp_bytes

        :return: the value of resp_bytes
        :rtype: float
        """
        return self.__resp_bytes

    def get_conn_state(self) -> str:
        """Getter of conn_state

        :return: the value of conn_state
        :rtype: str
        """
        return self.__conn_state

    def get_missed_bytes(self) -> float:
        """Getter of missed_bytes

        :return: the value of missed_bytes
        :rtype: float
        """
        return self.__missed_bytes

    def get_history(self) -> EventHistory:
        """Getter of history

        :return: the value of history
        :rtype: EventHistory
        """
        return self.__history

    def get_orig_pkts(self) -> float:
        """Getter of orig_pkts

        :return: the value of orig_pkts
        :rtype: float
        """
        return self.__orig_pkts

    def get_orig_ip_bytes(self) -> float:
        """Getter of orig_ip_bytes

        :return: the value of orig_ip_bytes
        :rtype: float
        """
        return self.__orig_ip_bytes

    def get_resp_pkts(self) -> float:
        """Getter of resp_pkts

        :return: the value of resp_pkts
        :rtype: float
        """
        return self.__resp_pkts

    def get_resp_ip_bytes(self) -> float:
        """Getter of resp_ip_bytes

        :return: the value of resp_ip_bytes
        :rtype: float
        """
        return self.__resp_ip_bytes

    def get_label(self) -> str:
        """Getter of label

        :return: the value of label
        :rtype: str
        """
        return self.__label


class Trace:
    """
    This class contains all the events that are being originated by the same
    ip and port of origin and responder hosts.

    :param orig_ip: ip of the host that started this trace
    :type orig_ip:  str
    :param orig_port: port of the host that started this trace
    :type orig_port: str
    :param resp_ip: ip of the host that has been requested to start this trace
    :type resp_ip: str
    :param resp_port: port of the host that has been requested to start this trace
    :type resp_port: str
    :param ts_on_open: timestamp of the first packet of the event that started this trace
    :type ts_on_open: str
    :param proto: protocol used for this trace
    :type proto: str
    :param events: list of the event between this 2 hosts with these ports
    :type events: list[Event]
    """

    def __init__(self, orig_ip: str, orig_port: int, resp_ip: str, resp_port: int, ts_on_open: str, proto: str):
        self.orig_ip = orig_ip
        self.orig_port = orig_port
        self.resp_ip = resp_ip
        self.resp_port = resp_port
        self.ts_on_open = ts_on_open
        self.proto = proto
        self.events = list()

    def add_packet(self, e: Event, elapsed_ts: float=None) -> None:
        """
        Class that contains multiple Events with the same id

        :param e: the event to be added to this wrapper
        :type e: Event
        :param elapsed_ts: max window time so that a event can be considered to belong to this Trace
        :type elapsed_ts: float
        :raises KeyError: raises a KeyError if the id of the event doesn't match
        """
        if elapsed_ts is None:
            if e.generate_id() == self.id:
                self.events.append(e)
            else:
                raise KeyError
        else:
            pass # TODO
    
    def to_json_obj(self) -> object:
        """Convert this object to an object that can be easily converted to a json

        :return: this object as a dumpable object
        :rtype: object
        """
        events = []
        for event in self.events:
            events.append(event.to_json_obj())

        return {
            'orig_ip': self.orig_ip,
            'orig_port': self.orig_port,
            'resp_ip': self.resp_ip,
            'resp_port': self.resp_port,
            'ts_on_open': self.ts_on_open,
            'proto': self.proto,
            'events': events,
        }
        
    def generate_id(self) -> str:
        """
        generate the id for this trace based on origin ip, origin port, responder ip, responder port, timestamp

        :return: the id based on the origin and responder ip and port
        :rtype: str
        """
        return f"{self.orig_ip} {self.orig_port} {self.resp_ip} {self.resp_port} {self.proto} {self.ts_on_open}"

    def get_list_of_ts(self) -> list:
        """Getter of the ts of the events in this trace

        :return: the list of all the value of ts
        :rtype: list[str]
        """
        list_ts = []
        for event in self.events:
            list_ts.append(event.get_ts())
        return list_ts

    def get_list_of_service(self) -> list:
        """Getter of the service of the events in this trace

        :return: the list of all the value of service
        :rtype: list[str]
        """
        list_service = []
        for event in self.events:
            list_service.append(event.get_service())
        return list_service

    def get_list_of_duration(self) -> list:
        """Getter of the duration of the events in this trace

        :return: the list of all the value of duration
        :rtype: list[float]
        """
        list_duration = []
        for event in self.events:
            list_duration.append(event.get_duration())
        return list_duration

    def get_list_of_orig_bytes(self) -> list:
        """Getter of the orig_bytes of the events in this trace

        :return: the list of all the value of orig_bytes
        :rtype: list[float]
        """
        list_orig_bytes = []
        for event in self.events:
            list_orig_bytes.append(event.get_orig_bytes())
        return list_orig_bytes

    def get_list_of_resp_bytes(self) -> list:
        """Getter of the resp_bytes of the events in this trace

        :return: the list of all the value of resp_bytes
        :rtype: list[float]
        """
        list_resp_bytes = []
        for event in self.events:
            list_resp_bytes.append(event.get_resp_bytes())
        return list_resp_bytes

    def get_list_of_conn_state(self) -> list:
        """Getter of the conn_state of the events in this trace

        :return: the list of all the value of conn_state
        :rtype: list[str]
        """
        list_conn_state = []
        for event in self.events:
            list_conn_state.append(event.get_conn_state())
        return list_conn_state

    def get_list_of_missed_bytes(self) -> list:
        """Getter of the missed_bytes of the events in this trace

        :return: the list of all the value of missed_bytes
        :rtype: list[float]
        """
        list_missed_bytes = []
        for event in self.events:
            list_missed_bytes.append(event.get_missed_bytes())
        return list_missed_bytes

    def get_list_of_history(self) -> list:
        """Getter of the history of the events in this trace

        :return: the list of all the value of history
        :rtype: list[EventHistory]
        """
        list_history = []
        for event in self.events:
            list_history.append(event.get_history())
        return list_history

    def get_list_of_orig_pkts(self) -> list:
        """Getter of the orig_pkts of the events in this trace

        :return: the list of all the value of orig_pkts
        :rtype: list[float]
        """
        list_orig_pkts = []
        for event in self.events:
            list_orig_pkts.append(event.get_orig_pkts())
        return list_orig_pkts

    def get_list_of_orig_ip_bytes(self) -> list:
        """Getter of the orig_ip_bytes of the events in this trace

        :return: the list of all the value of orig_ip_bytes
        :rtype: list[float]
        """
        list_orig_ip_bytes = []
        for event in self.events:
            list_orig_ip_bytes.append(event.get_orig_ip_bytes())
        return list_orig_ip_bytes

    def get_list_of_resp_pkts(self) -> list:
        """Getter of the resp_pkts of the events in this trace

        :return: the list of all the value of resp_pkts
        :rtype: list[float]
        """
        list_resp_pkts = []
        for event in self.events:
            list_resp_pkts.append(event.get_resp_pkts())
        return list_resp_pkts

    def get_list_of_resp_ip_bytes(self) -> list:
        """Getter of the resp_ip_bytes of the events in this trace

        :return: the list of all the value of resp_ip_bytes
        :rtype: list[float]
        """
        list_resp_ip_bytes = []
        for event in self.events:
            list_resp_ip_bytes.append(event.get_resp_ip_bytes())
        return list_resp_ip_bytes

    def get_list_of_label(self) -> list:
        """Getter of the label of the events in this trace

        :return: the list of all the value of label
        :rtype: list[str]
        """
        list_label = []
        for event in self.events:
            list_label.append(event.get_label())
        return list_label


class TracesController:
    """
    Class that contains the method used to filter and organize events

    :param path_of_file_input: path of the file that contains the logs to be acquired
    :type path_of_file_input: str, optional
    :param path_of_file_output: path of the file where the preprocessed lines are stored or will be stored
    :type path_of_file_output: str, optional
    :param path_of_file_json: path of the file where to write the json file
    :type path_of_file_json: str, optional
    :param lines_to_remove_ash: set of the # to remove from the file
    :type lines_to_remove_ash: set[str], optional
    :param strings_to_filter_event: set of string to be filtered out
    :type strings_to_filter_event: set[str], optional
    :param network_traffic: list of the Trace
    :type network_traffic: list[Trace]
    :param traces_pos_dict: dict that contains the indices of network_traffic
    :type traces_pos_dict: dict{str: int}
    """
    def __init__(self, 
        path_of_file_input: str='',
        path_of_file_output: str='',
        path_of_file_json: str='',
        lines_to_remove_ash: list=[],
        strings_to_filter_event: list=[]) -> None:
        """Constructor Method
        """
        self.path_of_file_input = path_of_file_input
        self.path_of_file_output = path_of_file_output
        self.path_of_file_json = path_of_file_json
        self.lines_to_remove_ash = lines_to_remove_ash
        self.strings_to_filter_event = strings_to_filter_event
        self.network_traffic = []
        self.traces_pos_dict = {}
    
    def load_paths_and_filters_from_config_file(self, config_file_path):
        """
        loads all path and filters form the ini file

        :param config_file_path: path of the configuration path
        :type config_file_path: str
        """   
        import configparser
        print('reading config option from file...')
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # checks if Files is in config.ini file
        if 'Files' in config:
            self.path_of_file_input = config['Files']['path_of_file_input'] if 'path_of_file_input' in config['Files'] else ''
            self.path_of_file_output = config['Files']['path_of_file_output'] if 'path_of_file_output' in config['Files'] else ''
            self.path_of_file_json = config['Files']['path_of_file_json']  if 'path_of_file_json' in config['Files'] else ''
        else:
            self.path_of_file_input = self.path_of_file_input if self.path_of_file_input != '' else ''
            self.path_of_file_output = self.path_of_file_output if self.path_of_file_output != '' else ''
            self.path_of_file_json = self.path_of_file_json if self.path_of_file_json != '' else ''

        # checks if Filters is in config.ini file
        if 'Filters' in config:
            self.lines_to_remove_ash = config['Filters']['lines_to_remove_ash']  if 'lines_to_remove_ash' in config['Filters'] else ''
            self.strings_to_filter_event = config['Filters']['strings_to_filter_event']  if 'strings_to_filter_event' in config['Filters'] else ''

            self.lines_to_remove_ash = self.lines_to_remove_ash.replace('\'', '').split(',')
            self.strings_to_filter_event = self.strings_to_filter_event.replace('\'', '').split(',')
        else:
            self.lines_to_remove_ash = '' 
            self.strings_to_filter_event = '' 

        print('...reading complete')


    def open_stored_preprocessed_lines(self) -> list:
        """
        read stored preprocessed lines from a file specified in the
        path_of_file_output of this object

        :return: pre-processed lines red from file
        :rtype: list(str)
        """
        print('reading stored lines from file...')
        with open(self.path_of_file_output, 'r') as f:
            self.preprocessed_lines = []
            for line in f:
                self.preprocessed_lines.append(line)

            print('...reading complete')
        return self.preprocessed_lines

    def print_preprocessed_lines_to_file(self):
        """
        prints preprocessed lines to a file specified in the path_of_file_output
        field of this object

        """
        print('printing preprocessed lines to file...')
        with open(self.path_of_file_output, 'w') as f_out:
            # writing lines to new file
            for line in self.preprocessed_lines:
                f_out.write(line)
        print('...printing complete')

    def normalize_lines(self) -> list:
        """
        normalize lines from file and if the path_of_file_output
        is set, prints the lines to a file

        :return: lines that have been normalized
        :rtype: list(str)
        """
        print('normalizing lines...')
        self.preprocessed_lines = []
        # normalizing lines
        with open(self.path_of_file_input, "r+") as f_in:
            for line in f_in:
                # removing comment lines
                to_remove = False
                for line_to_check in self.lines_to_remove:
                    if line.startswith(line_to_check):
                        to_remove = True
                if not(to_remove):
                    # replacing comment in field/types lines
                    for line_to_check in self.lines_to_remove_ash:
                        if line.startswith(line_to_check):
                            line = line.replace(line_to_check, '')
                            break

                    # removing unnecessary strings
                    for string in self.strings_to_filter_event: 
                        line = line.replace(string, '')
                    self.preprocessed_lines.append(line)
        print('...normalization completed')
        return self.preprocessed_lines

    def conv_lines_to_Trace_set(self) -> set:
        """
        Convert a list of preprocessed lines to a list of Event and inserts them into the 
        Trace set

        :return: set of strings that have been normalized
        :rtype: set(str)
        """
        print('converting preprocessed lines to list of traces...')
        packets = self.__conv_lines_to_list_of_Event()
        
        events_dict = {}
        for p in packets:
            id = p.generate_id()

            if id not in events_dict:
                events_dict[id] = Event()
            else:
                events_dict[id].add_packet(p)
        print('...conversion completed')
        self.events_list = list(events_dict.values())
        return self.events_list
        
    def __conv_lines_to_list_of_Event(self) -> list:
        """
        converts a list of preprocessed lines to a list of Events

        :return: list of Events converted from list of lines
        :rtype: list(Event)
        """
        packets = []
        
        for line in self.preprocessed_lines:
            packets.append(self.__conv_conn_line_to_Event(line))

        return packets

    def __conv_conn_line_to_Event(self, line: str) -> Event:
        """
        converts a conn.log line to a Event

        :param line: line to be converted to Event
        :type line: str
        :return: Event converted from line
        :rtype: Event
        """
        list_to_pack = line.split('\t')

        # getting info to insert in Event
        uid = list_to_pack[1]
        orig_ip = list_to_pack[2]
        orig_port = list_to_pack[3]
        resp_ip = list_to_pack[4]
        resp_port = list_to_pack[5]
        ts = list_to_pack[0]
        services = list_to_pack[7]
        state = list_to_pack[11]

        return Event(uid, orig_ip, orig_port, resp_ip, resp_port, ts, services, state)
        
    def print_Trace_list_to_json_file(self):
        """prints all the Traces list to a json file
        """
        print('writing the list of Events to a json file...')
        with open(self.path_of_file_json, 'w') as f:
            to_json = []
            for pw in self.events_list:
                to_json.append(pw.to_json_obj())
            
            json.dump(to_json, f, indent=4)
        print('...writing completed')


