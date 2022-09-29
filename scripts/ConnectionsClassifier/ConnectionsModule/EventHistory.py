from DiscretizerModule.Discretizer import Discretizer

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