from fastapi import FastAPI, APIRouter
import uvicorn
from scapy.all import IP, rdpcap, UDP
from datetime import datetime
from decimal import Decimal

app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/rip", tags=["Analysis"])

class RIPMessage:
    def __init__(self, timestamp, src_ip, dst_ip, rip_command):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.rip_command = rip_command 

def extract_rip_messages(pcap_file):
    packets = rdpcap(pcap_file)
    rip_messages = []
    for pkt in packets:
        if IP in pkt and UDP in pkt and pkt[UDP].dport == 520:
            rip_data = pkt[UDP].payload
            command = rip_data[0]
            rip_msg = RIPMessage(
                timestamp=pkt.time,
                src_ip=pkt[IP].src,
                dst_ip=pkt[IP].dst,
                rip_command=command
            )
            rip_messages.append(rip_msg)
    return rip_messages


pcap_file_path = './pcaps/rip.pcap'
rip_messages = extract_rip_messages(pcap_file_path)

@router.get("/all-data")
def get_all_data():
    total_messages = len(rip_messages)
    requests = len([msg for msg in rip_messages if msg.rip_command == 1])
    responses = len([msg for msg in rip_messages if msg.rip_command == 2])
    
    message_details = []
    failures = {}
    for msg in rip_messages:
        timestamp_float = float(msg.timestamp)
        message_details.append({
            "timestamp": datetime.utcfromtimestamp(timestamp_float).strftime('%Y-%m-%d %H:%M:%S'),
            "source_ip": msg.src_ip,
            "destination_ip": msg.dst_ip,
            "command_type": "Request" if msg.rip_command == 1 else "Response",
            "command_code": msg.rip_command
        })
        if msg.rip_command == 1: 
            key = f"{msg.src_ip} to {msg.dst_ip}"
            failures[key] = failures.get(key, 0) + 1

    return {
        "total_messages": total_messages,
        "requests": requests,
        "responses": responses,
        "message_details": message_details,
        "failures": failures
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
