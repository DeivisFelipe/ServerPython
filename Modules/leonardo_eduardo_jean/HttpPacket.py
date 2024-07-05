class HttpPacket:
    def __init__(self, source_ip, dest_ip, http_payload):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.http_payload = http_payload
