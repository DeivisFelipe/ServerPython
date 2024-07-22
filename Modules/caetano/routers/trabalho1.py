from fastapi import FastAPI, File, UploadFile
from typing import List
from scapy.all import IP, rdpcap
from fastapi import APIRouter
import uvicorn

router = APIRouter()

app = FastAPI()
nomes_protocolos = {
    1: "ICMP",
    6: "TCP",
    17: "UDP"
}

class IPData:
    def __init__(self, timestamp, src_ip, dst_ip, ttl, proto, length):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ttl = ttl
        self.proto = proto
        self.length = length

def extract_ip_info(pcap_file):
    packets = rdpcap(pcap_file)
    ip_packets = []
    
    for pkt in packets:
        if IP in pkt:
            ip_packet = pkt[IP]
            info = IPData(
                timestamp=pkt.time,
                src_ip=ip_packet.src,
                dst_ip=ip_packet.dst,
                ttl=ip_packet.ttl,
                proto=ip_packet.proto,
                length=ip_packet.len
            )
            ip_packets.append(info)
    
    return ip_packets

# Path to your pcapng file
pcap_file_path = './pcaps/trabalho1.pcapng'
ip_packets = extract_ip_info(pcap_file_path)

@router.get("/trabalho1")
def read_trabalho1():
    #faz uma relação de TTL e quantidade de pacotes
    ttl_dict = {}
    for ip in ip_packets:
        if ip.ttl in ttl_dict:
            ttl_dict[ip.ttl] += 1
        else:
            ttl_dict[ip.ttl] = 1
    ttl_protocol_dict = {}
    for ip in ip_packets:
        if ip.ttl in ttl_protocol_dict:
            if ip.proto in ttl_protocol_dict[ip.ttl]:
                #protocolo nome do protocolo
                
                ttl_protocol_dict[ip.ttl][ip.proto] += 1
            else:
                ttl_protocol_dict[ip.ttl][ip.proto] = 1
        else:
            ttl_protocol_dict[ip.ttl] = {}
            ttl_protocol_dict[ip.ttl][ip.proto] = 1
            
    
    return {
        "ttl_dict": ttl_dict,
        "ttl_protocol_dict": ttl_protocol_dict
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)  # Porta para o backend
