from dataclasses import dataclass, field
from scripts.Packet import Packet

@dataclass
class PacketWrapper:
    '''class that contains all the messages based on ip 
       and port of sender and receiver'''
    rig_ip: str
    orig_port: int
    resp_ip: str
    resp_port: int
    packets: list[Packet] = field(default_factory=list)

    # eq
    # init
    # repr

