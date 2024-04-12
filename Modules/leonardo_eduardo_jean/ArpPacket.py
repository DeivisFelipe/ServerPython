
class ArpPacket:
    def __init__(self, hardware_type, protocol_type, hardware_src, protocol_src, hardware_dst, protocol_dst, op):
        self.hardware_type = hardware_type
        self.protocol_type = protocol_type
        self.hardware_src = hardware_src
        self.protocol_src = protocol_src
        self.hardware_dst = hardware_dst
        self.protocol_dst = protocol_dst
        self.op = op
