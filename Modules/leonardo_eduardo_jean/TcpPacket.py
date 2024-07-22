class TcpPacket:
    def __init__(self, sport, dport, seq, ack, flags):
        self.sport = sport
        self.dport = dport
        self.seq = seq
        self.ack = ack
        self.flags = flags
