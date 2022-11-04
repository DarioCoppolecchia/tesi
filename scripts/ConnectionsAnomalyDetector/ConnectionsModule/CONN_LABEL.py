from enum import Enum, auto

class CONN_LABEL(Enum):
    """
    Possible labels that a Connection can have
        #. NULL
        #. ANOMALY
    """    
    NORMAL = auto()
    ANOMALY = auto()

    @classmethod
    def str_to_conn_label(cls, val: str) -> int:
        """converts a string to the relative enum

        :param val: string to be converted
        :type val: str
        :return: the value relative to the string
        :rtype: int
        """        
        if val == 'Normal':
            return cls.NORMAL
        elif val == 'Anomaly':
            return cls.ANOMALY
    
    @classmethod
    def conn_label_to_str(cls, conn_label: int) -> str:
        """converts an enum value to the relative string

        :param val: enum value to be converted
        :type val: int
        :return: the string relative to the value
        :rtype: str
        """  
        if conn_label == cls.NORMAL:
            return 'Normal'
        if conn_label == cls.ANOMALY:
            return 'Anomaly'