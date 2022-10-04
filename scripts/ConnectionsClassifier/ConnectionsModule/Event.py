from DiscretizerModule.Discretizer import Discretizer
from .EventHistory import EventHistory
from .CONN_STATE import CONN_STATE

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

    def __repr__(self):
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
        return self.__repr__()

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

    