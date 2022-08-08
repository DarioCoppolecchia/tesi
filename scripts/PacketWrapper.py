from dataclasses import dataclass, field
from Packet import Packet

@dataclass
class PacketWrapper:
    '''class that contains all the messages based on ip 
       and port of sender and receiver'''
    id: str
    packets: list[Packet] = field(default_factory=list)

    # eq
    # init
    # repr

