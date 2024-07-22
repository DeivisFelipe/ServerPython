from fastapi import FastAPI, File, UploadFile
from typing import List
from scapy.all import ARP, rdpcap
from fastapi import APIRouter
from collections import defaultdict
from manuf import manuf
import uvicorn

router = APIRouter()
parser = manuf.MacParser()
app = FastAPI()

class ARPData:
    def __init__(self, timestamp, src_ip, dst_ip, src_mac, dst_mac, op):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.op = op

def extract_arp_info(pcap_file):
    packets = rdpcap(pcap_file)
    arp_data_by_manufacturer = defaultdict(lambda: {"requests": 0, "replies": 0})
    #pega os pacotes ARP e pega o endereço MAC de origem e destino
    # e o tipo de operação (request ou reply)
      # Ler pacotes do arquivo PCAP
    packets = rdpcap(pcap_file)
    for packet in packets:
        if packet.haslayer(ARP):
            arp_layer = packet[ARP]
            src_mac = arp_layer.hwsrc
            dst_mac = arp_layer.hwdst
            src_manufacturer = parser.get_manuf(src_mac) or "Unknown"
            dst_manufacturer = parser.get_manuf(dst_mac) or "Unknown"
            
            if arp_layer.op == 1:  # ARP Request
                arp_data_by_manufacturer[src_manufacturer]["requests"] += 1
            elif arp_layer.op == 2:  # ARP Reply
                arp_data_by_manufacturer[dst_manufacturer]["replies"] += 1

    return arp_data_by_manufacturer

pcap_file_path = './pcaps/trabalho2.pcap'

@router.get("/trabalho2")
def read_trabalho2():
    # Path to your pcapng file
    arp_data_by_manufacturer = extract_arp_info(pcap_file_path)    
    return {
        "arp_data_by_manufacturer": arp_data_by_manufacturer
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)  # Porta para o backend
