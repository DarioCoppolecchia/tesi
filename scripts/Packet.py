from dataclasses import dataclass


@dataclass(frozen=True)
class Packet:
    '''Class of a single packet registered'''
    uid: str
    orig_ip: str
    orig_port: int
    resp_ip: str
    resp_port: int
    ts: str
    services: str
    state: str

    # compares are based on ip and port of origin and responder
    def __le__(self, other):
        if other.__class__ is self.__class__:
            return (self.orig_ip, self.orig_port, self.resp_ip, self.resp_port) <= (other.orig_ip, other.orig_port, other.resp_ip, other.resp_port)
        else:
            raise NotImplemented
    
    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return (self.orig_ip, self.orig_port, self.resp_ip, self.resp_port) < (other.orig_ip, other.orig_port, other.resp_ip, other.resp_port)
        else:
            raise NotImplemented

    def __gt__(self, other):
        if other.__class__ is self.__class__:
            return (self.orig_ip, self.orig_port, self.resp_ip, self.resp_port) > (other.orig_ip, other.orig_port, other.resp_ip, other.resp_port)
        else:
            raise NotImplemented

    def __ge__(self, other):
        if other.__class__ is self.__class__:
            return (self.orig_ip, self.orig_port, self.resp_ip, self.resp_port) >= (other.orig_ip, other.orig_port, other.resp_ip, other.resp_port)
        else:
            raise NotImplemented

    ## method generated by dataclass
    # delattr
    # eq
    # hash
    # init
    # repr
    # setattr
