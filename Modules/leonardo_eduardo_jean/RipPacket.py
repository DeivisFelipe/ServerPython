class RipPacket:
    def __init__(self, address_family, route_tag, ip_address, subnet_mask, next_hop, metric):
        self.address_family = address_family
        self.route_tag = route_tag
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.next_hop = next_hop
        self.metric = metric