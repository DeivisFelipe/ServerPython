from fastapi import FastAPI, Query, APIRouter
from typing import List
from scapy.all import rdpcap, IP, UDP
from scapy.layers.dns import DNS
from pydantic import BaseModel
from collections import Counter
import uvicorn

router = APIRouter()
app = FastAPI()

def extract_dns_info(pcap_file):
    packets = rdpcap(pcap_file)
    dns_queries = []
    top_n=10
    for packet in packets:
        if IP in packet and UDP in packet:
            if packet[UDP].dport == 53:  # DNS query port
                if DNS in packet and packet[DNS].qr == 0:  # DNS query
                    dns_query = packet[DNS].qd.qname.decode('utf-8')
                    dns_queries.append(dns_query)

    domain_counts = Counter(dns_queries)
    top_domains = domain_counts.most_common(top_n)
    return top_domains

pcap_file_path = '././pcaps/dns.pcap'
dns_packets = extract_dns_info(pcap_file_path)

@router.get("/trabalho7")
def read_trabalho7(skip: int = Query(0), limit: int = Query(10)):
    global dns_packets
    return dns_packets

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)
