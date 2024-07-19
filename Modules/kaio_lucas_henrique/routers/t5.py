from fastapi import FastAPI, APIRouter, HTTPException
import uvicorn
from scapy.all import IP, TCP, rdpcap
from datetime import datetime
from decimal import Decimal

app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/tcp", tags=["TCP Analysis"])

class TCPMessage:
    def __init__(self, timestamp, src_ip, dst_ip, src_port, dst_port, seq, ack, payload_len):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq = seq
        self.ack = ack
        self.payload_len = payload_len

def extract_tcp_messages(pcap_file):
    packets = rdpcap(pcap_file)
    tcp_messages = []
    for pkt in packets:
        if IP in pkt and TCP in pkt:
            ip_layer = pkt[IP]
            tcp_layer = pkt[TCP]
            payload_len = len(tcp_layer.payload)
            tcp_msg = TCPMessage(
                timestamp=pkt.time,
                src_ip=ip_layer.src,
                dst_ip=ip_layer.dst,
                src_port=tcp_layer.sport,
                dst_port=tcp_layer.dport,
                seq=tcp_layer.seq,
                ack=tcp_layer.ack,
                payload_len=payload_len
            )
            tcp_messages.append(tcp_msg)
    return tcp_messages

pcap_file_path = './pcaps/tcp.pcap'
tcp_messages = extract_tcp_messages(pcap_file_path)

@router.get("/all-data")
def get_all_tcp_data():
    traffic_volume = []
    connection_durations = {}
    for msg in tcp_messages:
        timestamp_float = float(Decimal(msg.timestamp))
        timestamp_formatted = datetime.utcfromtimestamp(timestamp_float).strftime('%Y-%m-%d %H:%M:%S')
        traffic_volume.append({"timestamp": timestamp_formatted, "payload_len": msg.payload_len})

        connection_key = f"{msg.src_ip}:{msg.dst_ip}:{msg.src_port}:{msg.dst_port}"
        if connection_key not in connection_durations:
            connection_durations[connection_key] = timestamp_float
        else:
            duration = timestamp_float - connection_durations[connection_key]
            connection_durations[connection_key] = duration  

    return {
        "traffic_volume": traffic_volume,
        "connection_durations": connection_durations
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
