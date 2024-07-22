from Modules.leonardo_eduardo_jean.Geolocation import IPGeolocation
from ipaddress import ip_address, IPv4Network

# Faixas de IPs privados
PRIVATE_IP_RANGES = [
    IPv4Network("10.0.0.0/8"),
    IPv4Network("172.16.0.0/12"),
    IPv4Network("192.168.0.0/16")
]

class IPv4Packet:
    def __init__(self, version, header_length, service_type, total_length, identification, flags, frag_offset, ttl,
                 protocol, checksum, src_ip, dst_ip, options=None):
        self.version = version
        self.header_length = header_length
        self.service_type = service_type
        self.total_length = total_length
        self.identification = identification
        self.flags = flags
        self.frag_offset = frag_offset
        self.ttl = ttl
        self.protocol = protocol
        self.checksum = checksum
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.options = options

    def is_public_ip(self, ip):
        # Verifica se o IP está fora das faixas de IPs privados
        for private_range in PRIVATE_IP_RANGES:
            if ip_address(ip) in private_range:
                return False
        return True

    def get_has_any_public_ip(self):
        return self.get_has_destiny_public_ip() or self.get_has_origin_public_ip()

    def get_destiny_location(self):
        try:
            if self.is_public_ip(self.dst_ip):
                location = IPGeolocation().get_geolocation(self.dst_ip)
                return {
                    "ip": self.dst_ip,
                    "latitude": location["latitude"],
                    "longitude": location["longitude"]
                }
            else:
                return {
                    "ip": self.dst_ip,
                    "latitude": None,
                    "longitude": None
                }
        except:
            return {
                "ip": self.dst_ip,
                "latitude": None,
                "longitude": None
            }

    def get_origin_location(self):
        try:
            if self.is_public_ip(self.src_ip):
                location = IPGeolocation().get_geolocation(self.src_ip)
                return {
                    "ip": self.src_ip,
                    "latitude": location["latitude"],
                    "longitude": location["longitude"]
                }
            return {
                "ip": self.src_ip,
                "latitude": None,
                "longitude": None
            }
        except:
            return {
                "ip": self.src_ip,
                "latitude": None,
                "longitude": None
            }

    def get_has_origin_public_ip(self):
        return self.is_public_ip(self.src_ip)

    def get_has_destiny_public_ip(self):
        return self.is_public_ip(self.dst_ip)
