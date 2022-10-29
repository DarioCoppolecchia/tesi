from enum import Enum, auto

class CONN_LABEL(Enum):
    """
    Possible labels that a Connection can have
        #. NULL
        #. FTP_PATATOR
        #. SSH_PATATOR
    """    
    NULL = auto()
    FTP_PATATOR = auto()
    SSH_PATATOR = auto()

    @classmethod
    def str_to_conn_label(cls, val: str) -> int:
        """converts a string to the relative enum

        :param val: string to be converted
        :type val: str
        :return: the value relative to the string
        :rtype: int
        """        
        if val == 'BENIGN':
            return cls.NULL
        elif val == 'FTP-Patator':
            return cls.FTP_PATATOR
        elif val == 'SSH-Patator':
            return cls.SSH_PATATOR
    
    @classmethod
    def conn_label_to_str(cls, conn_label: int) -> str:
        """converts an enum value to the relative string

        :param val: enum value to be converted
        :type val: int
        :return: the string relative to the value
        :rtype: str
        """  
        if conn_label == cls.NULL:
            return 'BENIGN'
        if conn_label == cls.FTP_PATATOR:
            return 'FTP-Patator'
        if conn_label == cls.SSH_PATATOR:
            return 'SSH-Patator'