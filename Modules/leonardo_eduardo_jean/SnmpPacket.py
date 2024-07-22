class SnmpPacket:
    def __init__(self, version, community, pdu_type, variable_bindings):
        self.version = version
        self.community = community
        self.pdu_type = pdu_type
        self.variable_bindings = variable_bindings

