import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from scapy.all import rdpcap, IP, RIP
from typing import List
from collections import defaultdict
router = APIRouter()
app = FastAPI()

def analyze_rip_packets(pcap_file):
    # Dicionário para armazenar informações de pacotes RIP
    rip_data = {
        "total_packets": 0,
        "request_packets": 0,
        "response_packets": 0,
        "routers": defaultdict(int),
        "routes": defaultdict(int)
    }

    # Ler pacotes do arquivo PCAP
    packets = rdpcap(pcap_file)
    for packet in packets:
        if RIP in packet:
            rip_layer = packet[RIP]
            rip_data["total_packets"] += 1
            if rip_layer.cmd == 1:
                rip_data["request_packets"] += 1
            elif rip_layer.cmd == 2:
                rip_data["response_packets"] += 1
            rip_data["routers"][packet[IP].src] += 1
    return rip_data
# Caminho para o arquivo pcap trabalho3 (assumindo conversão para .pcap)
pcap_file_path = './pcaps/trabalho3.pcap'

# Chama a função extract_rip_packets com o arquivo pcap desejado
rip_packets = analyze_rip_packets(pcap_file_path)

@router.get("/trabalho3")
def read_trabalho3():
    #devolve 
    rip_packets_list = []
    for router, count in rip_packets["routers"].items():
        print(router, count)
    return rip_packets
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)