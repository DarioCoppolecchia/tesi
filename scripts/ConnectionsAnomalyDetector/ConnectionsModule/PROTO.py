from enum import Enum, auto

class PROTO(Enum):
    """
    Describes the state that a Connection can have
        #. ICMP
        #. TCP
        #. UDP
    """    
    ICMP = auto()
    TCP = auto()
    UDP = auto()

    @classmethod
    def str_to_proto(cls, val: str) -> int:
        """converts a string to the relative enum

        :param val: string to be converted
        :type val: str
        :return: the value relative to the string
        :rtype: int
        """        
        if val == 'icmp':
            return cls.ICMP
        elif val == 'tcp':
            return cls.TCP
        elif val == 'udp':
            return cls.UDP
    
    @classmethod
    def proto_to_str(cls, proto: int) -> str:
        """converts an enum value to the relative string

        :param val: enum value to be converted
        :type val: int
        :return: the string relative to the value
        :rtype: str
        """  
        if proto == cls.ICMP:
            return 'icmp'
        if proto == cls.TCP:
            return 'tcp'
        if proto == cls.UDP:
            return 'udp'