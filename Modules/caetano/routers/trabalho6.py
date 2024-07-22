from fastapi import FastAPI, File, UploadFile
from typing import List
from scapy.all import rdpcap, IP, TCP
from fastapi import APIRouter
import uvicorn
from collections import Counter
from collections import defaultdict

router = APIRouter()

app = FastAPI()


def extract_http_info(pcap_file):
    packets = rdpcap(pcap_file)
    http_packets = []
    http_methods = {
        "GET": 0,
        "POST": 0,
        "PUT": 0,
        "DELETE": 0,
        "HEAD": 0,
        "OPTIONS": 0,
        "PATCH": 0,
        "UNKNOWN": 0
    }
    for pkt in packets:
        if IP in pkt and TCP in pkt:
            ip_packet = pkt[IP]
            tcp_packet = pkt[TCP]
            if tcp_packet.dport == 80 or tcp_packet.sport == 80:
            #separa por GET, POST, etc
                payload = bytes(pkt[TCP].payload)
                method = identify_http_method(payload)
                http_packet = {
                    "timestamp": pkt.time,
                    "src_ip": ip_packet.src,
                    "dst_ip": ip_packet.dst,
                    "src_port": tcp_packet.sport,
                    "dst_port": tcp_packet.dport,
                    "method": method,
                }
                if method:
                    http_methods[method] += 1
                else:
                    http_methods["UNKNOWN"] += 1
                http_packets.append(http_packet)
    
    return http_packets, http_methods
def identify_http_method(payload):
    # Decode the payload to a string
    http_payload = payload.decode("utf-8",errors="ignore")
    # Split the payload by lines
    lines = http_payload.split("\r\n")
    # The first line of an HTTP request contains the method
    first_line = lines[0]
    # Split the first line by spaces
    parts = first_line.split(" ")
    # The first part should be the HTTP method
    if parts[0] in ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]:
        return parts[0]
    else:
        return "UNKNOWN"

http_packets, methods = extract_http_info('././pcaps/trabalho6.pcap')

@router.get("/trabalho6")
def read_trabalho6():
    return {
        "http_packets": http_packets,
        "http_methods": methods
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)  # Porta para o backend

