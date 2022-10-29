from enum import Enum, auto

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