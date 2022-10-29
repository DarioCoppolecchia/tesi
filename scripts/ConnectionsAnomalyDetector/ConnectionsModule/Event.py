from DiscretizerModule.Discretizer import Discretizer
from .EventHistory import EventHistory
from .CONN_STATE import CONN_STATE

class Event:
    '''
    Class of a single event registered

    This class contains all of the data that are going to be used
    to classify an event

    :param ts: timestamp of this event
    :type ts: str
    :param service: An identification of an application protocol being sent over the event.
    :type service: str
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
            resp_ip_bytes: float) -> None:
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

    def __repr__(self) -> str:
        """returns a string version of this object

        :return: string version of this object
        :rtype: str
        """ 
        from datetime import datetime
        return f'''
    connection created at {datetime.fromtimestamp(float(self.__ts))}
    using the {self.__service} service
    lasted {self.__duration} seconds
    the originator sent {self.__orig_bytes} and the responder sent {self.__resp_bytes}
    the state of the connection is {CONN_STATE.state_to_str(self.__conn_state)}
    {self.__missed_bytes} bytes were missed during the lifetime of this connection
    the history of this connection is {self.__history.get_history()}
    the orginator sent {self.__orig_pkts} ({self.__orig_ip_bytes} bytes in the packet header)
    the orginator sent {self.__resp_pkts} ({self.__resp_ip_bytes} bytes in the packet header)
    
'''

    def __str__(self) -> str:
        """returns a string version of this object

        :return: string version of this object
        :rtype: str
        """ 
        return self.__repr__()

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

    ###### EVENT HISTORY ######

    def get_orig_syn(self) -> float:
        """Returns the value of this history objects orig_syn

        :return: the value of orig_syn
        :rtype: float
        """
        return self.__history.get_orig_syn()

    def get_orig_fin(self) -> float:
        """Returns the value of this history objects orig_fin

        :return: the value of orig_fin
        :rtype: float
        """
        return self.__history.get_orig_fin()

    def get_orig_syn_ack(self) -> float:
        """Returns the value of this objects history orig_syn_ack

        :return: the value of orig_syn_ack
        :rtype: float
        """
        return self.__history.get_orig_syn_ack()

    def get_orig_rst(self) -> float:
        """Returns the value of this history objects orig_rst

        :return: the value of orig_rst
        :rtype: float
        """
        return self.__history.get_orig_rst()

    def get_resp_syn(self) -> float:
        """Returns the value of this history objects resp_syn

        :return: the value of resp_syn
        :rtype: float
        """
        return self.__history.get_resp_syn()

    def get_resp_fin(self) -> float:
        """Returns the value of this history objects resp_fin

        :return: the value of resp_fin
        :rtype: float
        """
        return self.__history.get_resp_fin()

    def get_resp_syn_ack(self) -> float:
        """Returns the value of this objects history resp_syn_ack

        :return: the value of resp_syn_ack
        :rtype: float
        """
        return self.__history.get_resp_syn_ack()

    def get_resp_rst(self) -> float:
        """Returns the value of this history objects resp_rst

        :return: the value of resp_rst
        :rtype: float
        """
        return self.__history.get_resp_rst()

    def get_orig_ack(self) -> bool:
        """Returns the value of this objects orig_ack

        :return: the value of orig_ack
        :rtype: bool
        """
        return self.__history.get_orig_ack()
    def get_orig_payload(self) -> bool:
        """Returns the value of this objects orig_payload

        :return: the value of orig_payload
        :rtype: bool
        """
        return self.__history.get_orig_payload()
    def get_orig_inconsistent(self) -> bool:
        """Returns the value of this objects history  orig_inconsistent

        :return: the value of orig_inconsistent
        :rtype: bool
        """
        return self.__history.get_orig_inconsistent()
    def get_orig_multi_flag(self) -> bool:
        """Returns the value of this objects history  orig_multi_flag

        :return: the value of orig_multi_flag
        :rtype: bool
        """
        return self.__history.get_orig_multi_flag()
    def get_resp_ack(self) -> bool:
        """Returns the value of this objects history  resp_ack

        :return: the value of resp_ack
        :rtype: bool
        """
        return self.__history.get_resp_ack()
    def get_resp_payload(self) -> bool:
        """Returns the value of this objects history  resp_payload

        :return: the value of resp_payload
        :rtype: bool
        """
        return self.__history.get_resp_payload()
    def get_resp_inconsistent(self) -> bool:
        """Returns the value of this objects history  resp_inconsistent

        :return: the value of resp_inconsistent
        :rtype: bool
        """
        return self.__history.get_resp_inconsistent()
    def get_resp_multi_flag(self) -> bool:
        """Returns the value of this objects history  resp_multi_flag

        :return: the value of resp_multi_flag
        :rtype: bool
        """
        return self.__history.get_resp_multi_flag()

    def get_orig_bad_checksum(self) -> float:
        """Returns the value of this objects history orig_bad_checksum

        :return: the value of orig_bad_checksum
        :rtype: float
        """
        return self.__history.get_orig_bad_checksum()

    def get_orig_content_gap(self) -> float:
        """Returns the value of this objects history orig_content_gap

        :return: the value of orig_content_gap
        :rtype: float
        """
        return self.__history.get_orig_content_gap()

    def get_orig_retransmitted_payload(self) -> float:
        """Returns the value of this objects history orig_retransmitted_payload

        :return: the value of orig_retransmitted_payload
        :rtype: float
        """
        return self.__history.get_orig_retransmitted_payload()

    def get_orig_zero_window(self) -> float:
        """Returns the value of this objects history orig_zero_window

        :return: the value of orig_zero_window
        :rtype: float
        """
        return self.__history.get_orig_zero_window()

    def get_resp_bad_checksum(self) -> float:
        """Returns the value of this objects history resp_bad_checksum

        :return: the value of resp_bad_checksum
        :rtype: float
        """
        return self.__history.get_resp_bad_checksum()

    def get_resp_content_gap(self) -> float:
        """Returns the value of this objects history resp_content_gap

        :return: the value of resp_content_gap
        :rtype: float
        """
        return self.__history.get_resp_content_gap()

    def get_resp_retransmitted_payload(self) -> float:
        """Returns the value of this objects history resp_retransmitted_payload

        :return: the value of resp_retransmitted_payload
        :rtype: float
        """
        return self.__history.get_resp_retransmitted_payload()

    def get_resp_zero_window(self) -> float:
        """Returns the value of this objects history resp_zero_window

        :return: the value of resp_zero_window
        :rtype: float
        """
        return self.__history.get_resp_zero_window()

    def get_conn_dir_flipped(self) -> bool:
        """Returns the value of this objects history conn_dir_flipped

        :return: the value of conn_dir_flipped
        :rtype: bool
        """        
        return self.__history.get_conn_dir_flipped()

    ###### DISCRETIZED EVENT ######

    def get_discretized_duration(self) -> str:
        """Returns the discretized value of this objects duration

        :return: the discretized value of duration
        :rtype: str
        """
        if self.__duration == '-':
            self.__duration = 0
        return Event.disc_duration.discretize_attribute(float(self.__duration)) if Event.disc_duration is not None else 'n/a'
    
    def get_discretized_orig_bytes(self) -> str:
        """Returns the discretized value of this objects orig_bytes

        :return: the discretized value of orig_bytes
        :rtype: str
        """
        if self.__orig_bytes == '-':
            self.__orig_bytes = 0
        return Event.disc_orig_bytes.discretize_attribute(float(self.__orig_bytes)) if Event.disc_orig_bytes is not None else 'n/a'

    def get_discretized_resp_bytes(self) -> str:
        """Returns the discretized value of this objects resp_bytes

        :return: the discretized value of resp_bytes
        :rtype: str
        """
        if self.__resp_bytes == '-':
            self.__resp_bytes = 0
        return Event.disc_resp_bytes.discretize_attribute(float(self.__resp_bytes)) if Event.disc_resp_bytes is not None else 'n/a'

    def get_discretized_missed_bytes(self) -> str:
        """Returns the discretized value of this objects missed_bytes

        :return: the discretized value of missed_bytes
        :rtype: str
        """
        if self.__missed_bytes == '-':
            self.__missed_bytes = 0
        return Event.disc_missed_bytes.discretize_attribute(float(self.__missed_bytes)) if Event.disc_missed_bytes is not None else 'n/a'

    def get_discretized_orig_pkts(self) -> str:
        """Returns the discretized value of this objects orig_pkts

        :return: the discretized value of orig_pkts
        :rtype: str
        """
        if self.__orig_pkts == '-':
            self.__orig_pkts = 0
        return Event.disc_orig_pkts.discretize_attribute(float(self.__orig_pkts)) if Event.disc_orig_pkts is not None else 'n/a'

    def get_discretized_orig_ip_bytes(self) -> str:
        """Returns the discretized value of this objects orig_ip_bytes

        :return: the discretized value of orig_ip_bytes
        :rtype: str
        """
        if self.__orig_ip_bytes == '-':
            self.__orig_ip_bytes = 0
        return Event.disc_orig_ip_bytes.discretize_attribute(float(self.__orig_ip_bytes)) if Event.disc_orig_ip_bytes is not None else 'n/a'

    def get_discretized_resp_pkts(self) -> str:
        """Returns the discretized value of this objects resp_pkts

        :return: the discretized value of resp_pkts
        :rtype: str
        """
        if self.__resp_pkts == '-':
            self.__resp_pkts = 0
        return Event.disc_resp_pkts.discretize_attribute(float(self.__resp_pkts)) if Event.disc_resp_pkts is not None else 'n/a'

    def get_discretized_resp_ip_bytes(self) -> str:
        """Returns the discretized value of this objects resp_ip_bytes

        :return: the discretized value of resp_ip_bytes
        :rtype: str
        """
        if self.__resp_ip_bytes == '-':
            self.__resp_ip_bytes = 0
        return Event.disc_resp_ip_bytes.discretize_attribute(float(self.__resp_ip_bytes)) if Event.disc_resp_ip_bytes is not None else 'n/a'

    ###### DISCRETIZED HISTORY ######

    def get_discretized_orig_syn(self) -> str:
        """Returns the discretized value of this objects __history orig_syn

        :return: the discretized value of orig_syn
        :rtype: str
        """
        return self.__history.get_discretized_orig_syn()
    
    def get_discretized_orig_fin(self) -> str:
        """Returns the discretized value of this objects __history orig_fin

        :return: the discretized value of orig_fin
        :rtype: str
        """
        return self.__history.get_discretized_orig_fin()
    
    def get_discretized_orig_syn_ack(self) -> str:
        """Returns the discretized value of this objects __history orig_syn_ack

        :return: the discretized value of orig_syn_ack
        :rtype: str
        """
        return self.__history.get_discretized_orig_syn_ack()
    
    def get_discretized_orig_rst(self) -> str:
        """Returns the discretized value of this objects __history orig_rst

        :return: the discretized value of orig_rst
        :rtype: str
        """
        return self.__history.get_discretized_orig_rst()
    
    def get_discretized_resp_syn(self) -> str:
        """Returns the discretized value of this objects __history resp_syn

        :return: the discretized value of resp_syn
        :rtype: str
        """
        return self.__history.get_discretized_resp_syn()
    
    def get_discretized_resp_fin(self) -> str:
        """Returns the discretized value of this objects __history resp_fin

        :return: the discretized value of resp_fin
        :rtype: str
        """
        return self.__history.get_discretized_resp_fin()
    
    def get_discretized_resp_syn_ack(self) -> str:
        """Returns the discretized value of this objects __history resp_syn_ack

        :return: the discretized value of resp_syn_ack
        :rtype: str
        """
        return self.__history.get_discretized_resp_syn_ack()
    
    def get_discretized_resp_rst(self) -> str:
        """Returns the discretized value of this objects __history resp_rst

        :return: the discretized value of resp_rst
        :rtype: str
        """
        return self.__history.get_discretized_resp_rst()
    
    def get_discretized_orig_bad_checksum(self) -> str:
        """Returns the discretized value of this objects __history orig_bad_checksum

        :return: the discretized value of orig_bad_checksum
        :rtype: str
        """
        return self.__history.get_discretized_orig_bad_checksum()
    
    def get_discretized_orig_content_gap(self) -> str:
        """Returns the discretized value of this objects __history orig_content_gap

        :return: the discretized value of orig_content_gap
        :rtype: str
        """
        return self.__history.get_discretized_orig_content_gap()
    
    def get_discretized_orig_retransmitted_payload(self) -> str:
        """Returns the discretized value of this objects __history orig_retransmitted_payload

        :return: the discretized value of orig_retransmitted_payload
        :rtype: str
        """
        return self.__history.get_discretized_orig_retransmitted_payload()
    
    def get_discretized_orig_zero_window(self) -> str:
        """Returns the discretized value of this objects __history orig_zero_window

        :return: the discretized value of orig_zero_window
        :rtype: str
        """
        return self.__history.get_discretized_orig_zero_window()
    
    def get_discretized_resp_bad_checksum(self) -> str:
        """Returns the discretized value of this objects __history resp_bad_checksum

        :return: the discretized value of resp_bad_checksum
        :rtype: str
        """
        return self.__history.get_discretized_resp_bad_checksum()
    
    def get_discretized_resp_content_gap(self) -> str:
        """Returns the discretized value of this objects __history resp_content_gap

        :return: the discretized value of resp_content_gap
        :rtype: str
        """
        return self.__history.get_discretized_resp_content_gap()
    
    def get_discretized_resp_retransmitted_payload(self) -> str:
        """Returns the discretized value of this objects __history resp_retransmitted_payload

        :return: the discretized value of resp_retransmitted_payload
        :rtype: str
        """
        return self.__history.get_discretized_resp_retransmitted_payload()
    
    def get_discretized_resp_zero_window(self) -> str:
        """Returns the discretized value of this objects __history resp_zero_window

        :return: the discretized value of resp_zero_window
        :rtype: str
        """
        return self.__history.get_discretized_resp_zero_window()
    