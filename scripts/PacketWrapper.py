from dataclasses import dataclass, field
from Packet import Packet

@dataclass
class PacketWrapper:
    '''class that contains all the messages based on ip 
       and port of sender and receiver'''
    id: str
    packets: list[Packet] = field(default_factory=list)

    def add_packet(self, p: Packet) -> list:
        if p.generate_id() == self.id:
            return self.packets.append(p)
        else:
            raise KeyError
    
    def to_json_obj(self) -> object:
        packets = []
        for packet in self.packets:
            packets.append(packet.to_json_obj())

        return {
            "id": self.id,
            "packets": packets,
        }

    # eq
    # init
    # repr

