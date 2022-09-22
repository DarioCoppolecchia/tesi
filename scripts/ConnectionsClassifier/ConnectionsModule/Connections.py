import json
from enum import Enum, auto
from DiscretizerModule.Discretizer import Discretizer, Equal_Width_Discretizer, Equal_Height_Discretizer

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

    @classmethod
    def str_to_state(cls, val: str) -> int:
        """converts a string to the relative enum

        :param val: string to be converted
        :type val: str
        :return: the value relative to the string
        :rtype: int
        """        
        if val == 'S0':
            return cls.S0
        if val == 'S1':
            return cls.S1
        if val == 'SF':
            return cls.SF
        if val == 'REJ':
            return cls.REJ
        if val == 'S2':
            return cls.S2
        if val == 'S3':
            return cls.S3
        if val == 'RSTO':
            return cls.RSTO
        if val == 'RSTR':
            return cls.RSTR
        if val == 'RSTOS0':
            return cls.RSTOS0
        if val == 'RSTRH':
            return cls.RSTRH
        if val == 'SH':
            return cls.SH
        if val == 'SHR':
            return cls.SHR
        if val == 'OTH':
            return cls.OTH
    
    @classmethod
    def state_to_str(cls, state: int) -> str:
        """converts an enum value to the relative string

        :param val: enum value to be converted
        :type val: int
        :return: the string relative to the value
        :rtype: str
        """  
        if state == cls.S0:
            return 'S0'
        if state == cls.S1:
            return 'S1'
        if state == cls.SF:
            return 'SF'
        if state == cls.REJ:
            return 'REJ'
        if state == cls.S2:
            return 'S2'
        if state == cls.S3:
            return 'S3'
        if state == cls.RSTO:
            return 'RSTO'
        if state == cls.RSTR:
            return 'RSTR'
        if state == cls.RSTOS0:
            return 'RSTOS0'
        if state == cls.RSTRH:
            return 'RSTRH'
        if state == cls.SH:
            return 'SH'
        if state == cls.SHR:
            return 'SHR'
        if state == cls.OTH:
            return 'OTH'


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

    def __init__(self, history: str='') -> None:
        """The constructor initialize the parameters required and if history is given,
        it analyze the string and assigns the relativa values to the fields

        :param history: string to be analyzed, defaults to None
        :type history: str, optional
        """
        self.__history = history

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

    def get_history(self) -> str:
        """
        return the history string of this object

        :return: the value of history
        :rtype: str
        """
        return self.__history

    
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
    :type conn_state: CONN_STATE
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
    :param resp_ip_bytes: Number of IP level bytes that the responder sent (as seen on the wire, taken from the IP total_length header field)
    :type resp_ip_bytes: float
    :param label: label based on the originator ip and port, the responder ip and port, and the ts of this event
    :type label: float
    
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
    disc_duration: Discretizer = None
    disc_orig_bytes: Discretizer = None
    disc_resp_bytes: Discretizer = None
    disc_missed_bytes: Discretizer = None
    disc_orig_pkts: Discretizer = None
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
            history: str,
            orig_pkts: float,
            orig_ip_bytes: float,
            resp_pkts: float,
            resp_ip_bytes: float,
            label: str) -> None:
        """Constructor

        :param ts: timestamp of the event
        :type ts: str
        :param service: service of the event
        :type service: str
        :param duration: duration of the event
        :type duration: float
        :param orig_bytes: orig_bytes of the event
        :type orig_bytes: float
        :param resp_bytes: resp_bytes of the event
        :type resp_bytes: float
        :param conn_state: conn_state of the event
        :type conn_state: str
        :param missed_bytes: missed_bytes of the event
        :type missed_bytes: float
        :param history: history of the event
        :type history: str
        :param orig_pkts: orig_pkts of the event
        :type orig_pkts: float
        :param orig_ip_bytes: orig_ip_bytes of the event
        :type orig_ip_bytes: float
        :param resp_pkts: resp_pkts of the event
        :type resp_pkts: float
        :param resp_ip_bytes: resp_ip_bytes of the event
        :type resp_ip_bytes: float
        :param label: label of the event
        :type label: str
        """             
        self.__ts = ts
        self.__service = service
        self.__duration = duration
        self.__orig_bytes = orig_bytes
        self.__resp_bytes = resp_bytes
        self.__conn_state = CONN_STATE.str_to_state(conn_state)
        self.__missed_bytes = missed_bytes
        self.__history = EventHistory(history)
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
            'conn_state': CONN_STATE.state_to_str(self.__conn_state),
            'missed_bytes': self.__missed_bytes,
            'history': self.__history.get_history(),
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

    def get_conn_state(self) -> CONN_STATE:
        """Getter of conn_state

        :return: the value of conn_state
        :rtype: CONN_STATE
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
    ip and port of origin and responder hosts, and the same protocol.

    :param orig_ip: ip of the host that started this trace
    :type orig_ip:  str
    :param orig_port: port of the host that started this trace
    :type orig_port: int
    :param resp_ip: ip of the host that has been requested to start this trace
    :type resp_ip: str
    :param resp_port: port of the host that has been requested to start this trace
    :type resp_port: int
    :param proto: protocol used for this trace
    :type proto: str
    :param ts_on_open: timestamp of the first packet of the event that started this trace
    :type ts_on_open: str
    :param events: list of the event between this 2 hosts with these ports
    :type events: list[Event]
    """

    def __init__(self, orig_ip: str, orig_port: str, resp_ip: str, resp_port: str, proto: str,  ts_on_open: str):
        """Constructor

        :param orig_ip: orig_ip of this Trace
        :type orig_ip: str
        :param orig_port: orig_port of this Trace
        :type orig_port: str
        :param resp_ip: resp_ip of this Trace
        :type resp_ip: str
        :param resp_port: resp_port of this Trace
        :type resp_port: str
        :param proto: proto of this Trace
        :type proto: str
        :param ts_on_open: the ts of the first packet found with this id (orig_ip, orig_port, resp_ip, resp_port, port)
        :type ts_on_open: str
        """        
        self.orig_ip = orig_ip
        self.orig_port = int(orig_port)
        self.resp_ip = resp_ip
        self.resp_port = int(resp_port)
        self.proto = proto
        self.ts_on_open = ts_on_open
        self.events = list()

    def add_event(self, e: Event, elapsed_ts: float=None) -> bool:
        """
        Adds an event to this Trace. 
        If elapsed_ts is given, it checks if the event has been registered in the window of time
        between ts_on_open and ts_on_open + elapsed_ts

        :param e: the event to be added to this Trace
        :type e: Event
        :param elapsed_ts: max window time so that the event can be considered to belong to this Trace
        :type elapsed_ts: float
        """

        # Checking if the parameter is present
        if elapsed_ts is None:
            self.events.append(e)
            return True
        else:
            if float(elapsed_ts) <= float(e.get_ts()) - float(self.ts_on_open):
                self.events.append(e)
                return True
            return False
            
    
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
            'proto': self.proto,
            'ts_on_open': self.ts_on_open,
            'events': events,
        }
        
    @classmethod
    def generate_id_static(cls, orig_ip: str=None, orig_port: int=None, resp_ip: str=None, resp_port: int=None, proto: str=None) -> str:
        """
        generate the id for this trace based on origin ip, origin port, responder ip, responder port and protocol values of the parameters

        :param orig_ip: orig_ip to be inserted in the id, defaults to None
        :type orig_ip: str, optional
        :param orig_port: orig_port to be inserted in the id, defaults to None
        :type orig_port: int, optional
        :param resp_ip: resp_ip to be inserted in the id, defaults to None
        :type resp_ip: str, optional
        :param resp_port: resp_port to be inserted in the id, defaults to None
        :type resp_port: int, optional
        :param proto: proto to be inserted in the id, defaults to None
        :type proto: str, optional
        :return: generated id 
        :rtype: str
        """        
        return f"{orig_ip} {orig_port} {resp_ip} {resp_port} {proto}"

    def generate_id(self) -> str:
        """
        generate the id for this trace based on origin ip, origin port, responder ip, responder port and protocol of this oject

        :return: the id based on the origin and responder ip and port and the protocol
        :rtype: str
        """
        return Trace.generate_id_static(self.orig_ip, self.orig_port, self.resp_ip, self.resp_port, self.proto)

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
        :rtype: list[CONN_STATE]
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
    Class that contains the method used to filter and organize events and traces

    :param path_of_file_input: path of the file that contains the logs to be acquired
    :type path_of_file_input: str
    :param path_of_file_output: path of the file where the preprocessed lines are stored or will be stored
    :type path_of_file_output: str
    :param path_of_file_json: path of the file where to write the json file
    :type path_of_file_json: str
    :param lines_to_remove_ash: set of the # to remove from the file
    :type lines_to_remove_ash: set[str]
    :param strings_to_filter_event: set of string to be filtered out
    :type strings_to_filter_event: set[str]
    :param network_traffic: list of the Trace
    :type network_traffic: list[Trace]
    :param traces_pos_dict: dict that contains the indices of network_traffic
    :type traces_pos_dict: dict{str: int}
    """
    def __init__(self, 
        path_of_file_input: str='',
        path_of_file_output: str='',
        path_of_file_json: str='',
        lines_to_remove_ash: set=set(),
        strings_to_filter_event: set=set()) -> None:
        """Constructor method

        :param path_of_file_input: path of the file from where to get the events, defaults to ''
        :type path_of_file_input: str, optional
        :param path_of_file_output: path of the file where to store the preprocessed lines, defaults to ''
        :type path_of_file_output: str, optional
        :param path_of_file_json: path of the file where to dump the traces converted to json, defaults to ''
        :type path_of_file_json: str, optional
        :param lines_to_remove_ash: set of the strings that if match the start of a line in the input file, that substring will be removed (this doesn't delete it from the input file), defaults to set()
        :type lines_to_remove_ash: set, optional
        :param strings_to_filter_event: set of the substring to be removed from the lines read in the file (this doesn't delete it from the input file), defaults to set()
        :type strings_to_filter_event: set, optional
        """
        self.path_of_file_input = path_of_file_input
        self.path_of_file_output = path_of_file_output
        self.path_of_file_json = path_of_file_json
        self.lines_to_remove_ash = lines_to_remove_ash
        self.strings_to_filter_event = strings_to_filter_event
        self.network_traffic = []
        self.traces_pos_dict = {}
    
    def load_paths_and_filters_from_config_file(self, config_file_path: str) -> None:
        """
        Loads all path and filters form the .ini file

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

    def print_preprocessed_lines_to_file(self) -> None:
        """
        prints preprocessed lines to a file specified in the path_of_file_output
        field of this object

        """
        print('printing preprocessed lines to file...')
        with open(self.path_of_file_output, 'w') as f_out:
            # writing lines to new file
            for line in self.preprocessed_lines:
                f_out.write(line + '\n')
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
            lines_to_remove = [
                '#separator',
                '#set_separator',
                '#empty_field',
                '#unset_field',
                '#path',
                '#open',
                '#types',
                '#close',
            ]
            for line in f_in:
                # removing comment lines
                to_remove = False
                for line_to_check in lines_to_remove:
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
                    self.preprocessed_lines.append(line.replace('\n', ''))
        print('...normalization completed')
        return self.preprocessed_lines

    def conv_lines_to_Trace_list(self) -> list:
        """
        Convert a list of preprocessed lines to a list of Event and inserts them into the 
        Trace list

        :return: list of strings that have been normalized
        :rtype: list(Traces)
        """
        print('converting preprocessed lines to list of traces...')
        count = 0
        for line in self.preprocessed_lines[1:]:
            list_to_pack = line.split('\t')

            ts = list_to_pack[0]
            orig_ip = list_to_pack[2]
            orig_port = list_to_pack[3]
            resp_ip = list_to_pack[4]
            resp_port = list_to_pack[5]
            proto = list_to_pack[6]
            service = list_to_pack[7]
            duration = list_to_pack[8]
            orig_bytes = list_to_pack[9]
            resp_bytes = list_to_pack[10]
            conn_state = list_to_pack[11]
            missed_bytes = list_to_pack[14]
            history = list_to_pack[15]
            orig_pkts = list_to_pack[16]
            orig_ip_bytes = list_to_pack[17]
            resp_pkts = list_to_pack[18]
            resp_ip_bytes = list_to_pack[19]
            label = list_to_pack[21]

            event = Event(ts,
                service,
                duration,
                orig_bytes,
                resp_bytes,
                conn_state,
                missed_bytes,
                history,
                orig_pkts,
                orig_ip_bytes,
                resp_pkts,
                resp_ip_bytes,
                label)
        
            id = Trace.generate_id_static(orig_ip, orig_port, resp_ip, resp_port, proto)

            if id not in self.traces_pos_dict:
                self.network_traffic.append(Trace(orig_ip, orig_port, resp_ip, resp_port, proto, ts))
                self.network_traffic[-1].add_event(event)
                self.traces_pos_dict[id] = count
                count += 1
            else:
                self.network_traffic[self.traces_pos_dict[id]].add_event(event)
        print('...conversion completed')
    
    '''
    
    '''
    def apply_label_to_events_in_file(self, constraint_to_label: list) -> None:
        """
        this function applies the label according by the rules in the parameter. The constraints must have timestamp upper bound and lower bound, ip of the attacker, ip of the attacked and the label. If the row doesn't follow the constraint, the label will be BENIGN

        The rules are described as follows
        :math:`label(x) <- 
            | lower_bound <= x.ts <= upper_bound && 
            | ip_attacker = x.ip_orig && 
            | ip_attacked = x.ip_resp`

        The structure of the constraint will be a list of dict, where the keys will be 
            * lower_bound, 
            * upper_bound, 
            * ip_attacker, 
            * ip_attacked, 
            * label
        and the values will be the corresponding values

        An example of the structure
        | interval_to_label = [
        |     { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
        |     { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
        |     ...
        |     { lower_bound, upper_bound, ip_attacker, ip_attacked, label },
        | ]

        :param constraint_to_label: constraint to follow to apply the label correctly
        :type constraint_to_label: list
        """
        print('applying label to the file...')
        file = self.path_of_file_input.replace('_labeled', '')
        with open(file, 'r') as f:
            lines = f.readlines()
            del lines[:6]
            del lines[1]
            del lines[-1]
            lines[0] = lines[0].replace("#fields\t", "")
        with open(file, 'w') as f:
            f.writelines(lines)
        with open(self.path_of_file_input, 'w') as f_out:
            with open(file, 'r') as f_in:
                next(f_in)
                for line in f_in:
                    line = line.replace('\n', '')
                    splitted = line.split('\t')
                    ts = splitted[0]
                    orig_ip = splitted[2]
                    resp_ip = splitted[4]
                    for constraints in constraint_to_label:
                        if (float(constraints['lower_bound']) <= float(ts) <= float(constraints['upper_bound']) and
                            constraints['ip_attacker'] == orig_ip and
                            constraints['ip_attacked'] == resp_ip):
                            line += '\t' + constraints['label']
                            break
                    else:
                        line += '\t' + 'BENIGN'
                    f_out.write(line + '\n')
        print('...label application completed')
        
    def print_Trace_list_to_json_file(self) -> None:
        """prints all the Traces list to a json file
        """
        print('writing the list of Events to a json file...')
        with open(self.path_of_file_json, 'w') as f:
            to_json = []
            for trace in self.network_traffic:
                to_json.append(trace.to_json_obj())
            
            json.dump(to_json, f, indent=4)
        print('...writing completed')

    def __get_list_of_all_attributes(self, attributes_list: list) -> dict:
        """Creates a dictionary of list of the values of each attribute

        Possible values of the attributes_list:
            #. orig_bytes
            #. resp_bytes
            #. missed_bytes
            #. orig_pkts
            #. duration
            #. orig_ip_bytes
            #. resp_pkts
            #. resp_ip_bytes

        :param attributes_list: list of the attributes from where to collect data from
        :type attributes_list: list
        :return: dictionary of list of the attributes of all item
        :rtype: dict
        """

        attributes_value_dict = {}
        for attribute in attributes_list:
            attributes_value_dict[attribute] = []

        orig_bytes_list = []
        resp_bytes_list = []
        missed_bytes_list = []
        orig_pkts_list = []
        duration_list = []
        orig_ip_bytes_list = []
        resp_pkts_list = []
        resp_ip_bytes_list = []

        # getting all value for each list
        if 'orig_bytes' in attributes_value_dict:
            for trace in self.network_traffic:
                orig_bytes_list += trace.get_list_of_orig_bytes()
        if 'resp_bytes' in attributes_value_dict:
            for trace in self.network_traffic:
                resp_bytes_list += trace.get_list_of_resp_bytes()
        if 'missed_bytes' in attributes_value_dict:
            for trace in self.network_traffic:
                missed_bytes_list += trace.get_list_of_missed_bytes()
        if 'orig_pkts' in attributes_value_dict:
            for trace in self.network_traffic:
                orig_pkts_list += trace.get_list_of_orig_pkts()
        if 'duration' in attributes_value_dict:
            for trace in self.network_traffic:
                duration_list += trace.get_list_of_duration()
        if 'orig_ip_bytes' in attributes_value_dict:
            for trace in self.network_traffic:
                orig_ip_bytes_list += trace.get_list_of_orig_ip_bytes()
        if 'resp_pkts' in attributes_value_dict:
            for trace in self.network_traffic:
                resp_pkts_list += trace.get_list_of_resp_pkts()
        if 'resp_ip_bytes' in attributes_value_dict:
            for trace in self.network_traffic:
                resp_ip_bytes_list += trace.get_list_of_resp_ip_bytes()

        return orig_bytes_list, resp_bytes_list, missed_bytes_list, orig_pkts_list, duration_list, orig_ip_bytes_list, resp_pkts_list, resp_ip_bytes_list


    def discretize_attributes_equal_width(self, n_bins_dict: dict) -> None:
        """Discretizes all the attribute with equal width discretization

        Possible values of the attributes_list:
            #. orig_bytes
            #. resp_bytes
            #. missed_bytes
            #. orig_pkts
            #. duration
            #. orig_ip_bytes
            #. resp_pkts
            #. resp_ip_bytes

        :param n_bins_dict: dictionary where the key is the attribute to witch apply discretization and the value is the number of bins for that attribute
        :type n_bins_dict: dict
        """        
        attribute_to_discretize = list(n_bins_dict.keys())
        
        if 'orig_bytes' in attribute_to_discretize:
            Event.disc_orig_bytes = Equal_Width_Discretizer(n_bins_dict['orig_bytes'])
        if 'resp_bytes' in attribute_to_discretize:
            Event.disc_resp_bytes = Equal_Width_Discretizer(n_bins_dict['resp_bytes'])
        if 'missed_bytes' in attribute_to_discretize:
            Event.disc_missed_bytes = Equal_Width_Discretizer(n_bins_dict['missed_bytes'])
        if 'orig_pkts' in attribute_to_discretize:
            Event.disc_orig_pkts = Equal_Width_Discretizer(n_bins_dict['orig_pkts'])
        if 'duration' in attribute_to_discretize:
            Event.disc_duration = Equal_Width_Discretizer(n_bins_dict['duration'])
        if 'orig_ip_bytes' in attribute_to_discretize:
            Event.disc_orig_ip_bytes = Equal_Width_Discretizer(n_bins_dict['orig_ip_bytes'])
        if 'resp_pkts' in attribute_to_discretize:
            Event.disc_resp_pkts = Equal_Width_Discretizer(n_bins_dict['resp_pkts'])
        if 'resp_ip_bytes' in attribute_to_discretize: 
            Event.disc_resp_ip_bytes = Equal_Width_Discretizer(n_bins_dict['resp_ip_bytes'])
        
        # TODO effettuare discretizzazione

    def discretize_attributes_equal_height(self, n_bins_dict: dict) -> None:
        """Discretizes all the attribute with equal height discretization

        Possible values of the attributes_list:
            #. orig_bytes
            #. resp_bytes
            #. missed_bytes
            #. orig_pkts
            #. duration
            #. orig_ip_bytes
            #. resp_pkts
            #. resp_ip_bytes

        :param n_bins_dict: dictionary where the key is the attribute to witch apply discretization and the value is the number of bins for that attribute
        :type n_bins_dict: dict
        """
        attributes_list = list(n_bins_dict.keys())
        
        if 'orig_bytes' in attributes_list:
            Event.disc_orig_bytes = Equal_Height_Discretizer(attributes_list['orig_bytes'])
        if 'resp_bytes' in attributes_list:
            Event.disc_resp_bytes = Equal_Height_Discretizer(attributes_list['resp_bytes'])
        if 'missed_bytes' in attributes_list:
            Event.disc_missed_bytes = Equal_Height_Discretizer(attributes_list['missed_bytes'])
        if 'orig_pkts' in attributes_list:
            Event.disc_orig_pkts = Equal_Height_Discretizer(attributes_list['orig_pkts'])
        if 'duration' in attributes_list:
            Event.disc_duration = Equal_Height_Discretizer(attributes_list['duration'])
        if 'orig_ip_bytes' in attributes_list:
            Event.disc_orig_ip_bytes = Equal_Height_Discretizer(attributes_list['orig_ip_bytes'])
        if 'resp_pkts' in attributes_list:
            Event.disc_resp_pkts = Equal_Height_Discretizer(attributes_list['resp_pkts'])
        if 'resp_ip_bytes' in attributes_list: 
            Event.disc_resp_ip_bytes = Equal_Height_Discretizer(attributes_list['resp_ip_bytes'])

        # TODO effettuare discretizzazione
