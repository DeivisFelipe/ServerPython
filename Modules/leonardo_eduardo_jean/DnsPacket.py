class DnsPacket:
    def __init__(self, transaction_id, query_name, query_type, query_class, response_code):
        self.transaction_id = transaction_id
        self.query_name = query_name
        self.query_type = query_type
        self.query_class = query_class
        self.response_code = response_code
