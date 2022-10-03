from .Event import Event
from .PROTO import PROTO

class Trace:
    """
    This class contains all the events that are being originated by the same
    ip and port of origin and responder hosts, and the same protocol.

    :param __orig_ip: ip of the host that started this trace
    :type __orig_ip:  str
    :param __orig_port: port of the host that started this trace
    :type __orig_port: int
    :param __resp_ip: ip of the host that has been requested to start this trace
    :type __resp_ip: str
    :param __resp_port: port of the host that has been requested to start this trace
    :type __resp_port: int
    :param __proto: protocol used for this trace
    :type __proto: PROTO
    :param __ts_on_open: timestamp of the first packet of the event that started this trace
    :type __ts_on_open: str
    :param __events: list of the event between this 2 hosts with these ports
    :type __events: list[Event]
    :param label: label based on the originator ip and port, the responder ip and port, and the ts of this trace
    :type label: float
    """

    def __init__(self, orig_ip: str, orig_port: str, resp_ip: str, resp_port: str, proto: str, ts_on_open: str, label: str):
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
        :param label: label based on the originator ip and port, the responder ip and port, and the ts of this trace
        :type label: float
        """        
        self.__orig_ip: str = orig_ip
        self.__orig_port: int = int(orig_port)
        self.__resp_ip: str = resp_ip
        self.__resp_port: int = int(resp_port)
        self.__proto: PROTO = PROTO.str_to_proto(proto)
        self.__ts_on_open: str = ts_on_open
        self.__label: str = label
        self.__events: list = []

    def __repr__(self):
        from datetime import datetime
        return f'''
traces of connection {self.__orig_ip}:{self.__orig_port} {self.__resp_ip}:{self.__resp_port}
with protocol: {self.__proto}
first packet sent in: {datetime.fromtimestamp(self.__ts_on_open)}
with label: {self.__label}
''' + '\n    '.join([str(e) for e in self.__events])

    def __str__(self) -> str:
        return self.__repr__()

    def get_orig_ip(self) -> str:
        """returns the orig_ip value of this object

        :return: the value of the orig_ip attribute
        :rtype: str
        """        
        return self.__orig_ip

    def get_orig_port(self) -> int:
        """returns the orig_port value of this object

        :return: the value of the orig_port attribute
        :rtype: int
        """        
        return self.__orig_port

    def get_resp_ip(self) -> str:
        """returns the resp_ip value of this object

        :return: the value of the resp_ip attribute
        :rtype: str
        """        
        return self.__resp_ip

    def get_resp_port(self) -> int:
        """returns the resp_port value of this object

        :return: the value of the resp_port attribute
        :rtype: int
        """        
        return self.__resp_port

    def get_proto(self) -> PROTO:
        """returns the proto value of this object

        :return: the value of the proto attribute
        :rtype: PROTO
        """        
        return self.__proto

    def get_ts_on_open(self) -> str:
        """returns the ts_on_open value of this object

        :return: the value of the ts_on_open attribute
        :rtype: str
        """        
        return self.__ts_on_open

    def get_label(self) -> str:
        """Getter of label

        :return: the value of label
        :rtype: str
        """
        return self.__label

    def get_events(self) -> list:
        """returns the events value of this object

        :return: the value of the events attribute
        :rtype: list
        """        
        return self.__events

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
            self.__events.append(e)
            return True
        else:
            if float(elapsed_ts) <= float(e.get_ts()) - float(self.__ts_on_open):
                self.__events.append(e)
                return True
            return False
            
    
    def to_json_obj(self) -> object:
        """Convert this object to an object that can be easily converted to a json

        :return: this object as a dumpable object
        :rtype: object
        """
        return {
            'orig_ip': self.__orig_ip,
            'orig_port': self.__orig_port,
            'resp_ip': self.__resp_ip,
            'resp_port': self.__resp_port,
            'proto': PROTO.proto_to_str(self.__proto),
            'ts_on_open': self.__ts_on_open,
            'label': self.label,
            'events': [event.to_json_obj() for event in self.__events],
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
        return f"{orig_ip} {orig_port} {resp_ip} {resp_port} {PROTO.str_to_proto(proto)}"

    def generate_id(self) -> str:
        """
        generate the id for this trace based on origin ip, origin port, responder ip, responder port and protocol of this oject

        :return: the id based on the origin and responder ip and port and the protocol
        :rtype: str
        """
        return Trace.generate_id_static(self.__orig_ip, self.__orig_port, self.__resp_ip, self.__resp_port, self.__proto)

    def get_list_of_ts(self) -> list:
        """Getter of the ts of the events in this trace

        :return: the list of all the value of ts
        :rtype: list[str]
        """
        return [event.get_ts() for event in self.__events]

    def get_list_of_service(self) -> list:
        """Getter of the service of the events in this trace

        :return: the list of all the value of service
        :rtype: list[str]
        """
        return [event.get_service() for event in self.__events]

    def get_list_of_duration(self) -> list:
        """Getter of the duration of the events in this trace

        :return: the list of all the value of duration
        :rtype: list[float]
        """
        return [event.get_duration() for event in self.__events]

    def get_list_of_orig_bytes(self) -> list:
        """Getter of the orig_bytes of the events in this trace

        :return: the list of all the value of orig_bytes
        :rtype: list[float]
        """
        return [event.get_orig_bytes() for event in self.__events]

    def get_list_of_resp_bytes(self) -> list:
        """Getter of the resp_bytes of the events in this trace

        :return: the list of all the value of resp_bytes
        :rtype: list[float]
        """
        return [event.get_resp_bytes() for event in self.__events]

    def get_list_of_conn_state(self) -> list:
        """Getter of the conn_state of the events in this trace

        :return: the list of all the value of conn_state
        :rtype: list[CONN_STATE]
        """
        return [event.get_conn_state() for event in self.__events]

    def get_list_of_missed_bytes(self) -> list:
        """Getter of the missed_bytes of the events in this trace

        :return: the list of all the value of missed_bytes
        :rtype: list[float]
        """
        return [event.get_missed_bytes() for event in self.__events]

    def get_list_of_history(self) -> list:
        """Getter of the history of the events in this trace

        :return: the list of all the value of history
        :rtype: list[EventHistory]
        """
        return [event.get_history() for event in self.__events]

    def get_list_of_orig_pkts(self) -> list:
        """Getter of the orig_pkts of the events in this trace

        :return: the list of all the value of orig_pkts
        :rtype: list[float]
        """
        return [event.get_orig_pkts() for event in self.__events]

    def get_list_of_orig_ip_bytes(self) -> list:
        """Getter of the orig_ip_bytes of the events in this trace

        :return: the list of all the value of orig_ip_bytes
        :rtype: list[float]
        """
        return [event.get_orig_ip_bytes() for event in self.__events]

    def get_list_of_resp_pkts(self) -> list:
        """Getter of the resp_pkts of the events in this trace

        :return: the list of all the value of resp_pkts
        :rtype: list[float]
        """
        return [event.get_resp_pkts() for event in self.__events]

    def get_list_of_resp_ip_bytes(self) -> list:
        """Getter of the resp_ip_bytes of the events in this trace

        :return: the list of all the value of resp_ip_bytes
        :rtype: list[float]
        """
        return [event.get_resp_ip_bytes() for event in self.__events]

    def get_list_of_discretized_duration(self) -> list:
        """Getter of the discretized duration in this trace

        :return: the list of all the discretized value of duration
        :rtype: list
        """
        return [event.get_discretized_duration() for event in self.__events]

    def get_list_of_discretized_orig_bytes(self) -> list:
        """Getter of the discretized orig_bytes in this trace

        :return: the list of all the discretized value of orig_bytes
        :rtype: list
        """
        return [event.get_discretized_orig_bytes() for event in self.__events]
        
    def get_list_of_discretized_resp_bytes(self) -> list:
        """Getter of the discretized resp_bytes in this trace

        :return: the list of all the discretized value of resp_bytes
        :rtype: list
        """
        return [event.get_discretized_resp_bytes() for event in self.__events]
        
    def get_list_of_discretized_missed_bytes(self) -> list:
        """Getter of the discretized missed_bytes in this trace

        :return: the list of all the discretized value of missed_bytes
        :rtype: list
        """
        return [event.get_discretized_missed_bytes() for event in self.__events]
        
    def get_list_of_discretized_orig_pkts(self) -> list:
        """Getter of the discretized orig_pkts in this trace

        :return: the list of all the discretized value of orig_pkts
        :rtype: list
        """
        return [event.get_discretized_orig_pkts() for event in self.__events]
        
    def get_list_of_discretized_orig_ip_bytes(self) -> list:
        """Getter of the discretized orig_ip_bytes in this trace

        :return: the list of all the discretized value of orig_ip_bytes
        :rtype: list
        """
        return [event.get_discretized_orig_ip_bytes() for event in self.__events]
        
    def get_list_of_discretized_resp_pkts(self) -> list:
        """Getter of the discretized resp_pkts in this trace

        :return: the list of all the discretized value of resp_pkts
        :rtype: list
        """
        return [event.get_discretized_resp_pkts() for event in self.__events]
        
    def get_list_of_discretized_resp_ip_bytes(self) -> list:
        """Getter of the discretized resp_ip_bytes in this trace

        :return: the list of all the discretized value of resp_ip_bytes
        :rtype: list
        """
        return [event.get_discretized_resp_ip_bytes() for event in self.__events]
    
    