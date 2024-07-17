from fastapi import FastAPI, APIRouter
from scapy.all import rdpcap, ARP
from pydantic import BaseModel
import threading
import uvicorn

# Inicializa o FastAPI
app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/arp", tags=["Analysis"])

class ARPData(BaseModel):
    source_ip: str
    destination_ip: str
    source_mac: str
    destination_mac: str
    operation: str

arp_data_storage = []


pcap_file_path = './pcaps/trabalho2.pcap'


def capture_arp_packets():
    packets = rdpcap(pcap_file_path)
    for packet in packets:
        if ARP in packet and packet[ARP].op in (1, 2):
            arp_data = {
                'source_ip': packet[ARP].psrc,
                'destination_ip': packet[ARP].pdst,
                'source_mac': packet[ARP].hwsrc,
                'destination_mac': packet[ARP].hwdst,
                'operation': 'request' if packet[ARP].op == 1 else 'reply'
            }
            arp_data_storage.append(arp_data)
    return arp_data_storage

@router.on_event("startup")
def start_arp_capture():
    thread = threading.Thread(target=capture_arp_packets)
    thread.start()

@router.get("/arp-data", response_model=list[ARPData])
def get_arp_data():
    return arp_data_storage


app.include_router(router)


from dotenv import load_dotenv
load_dotenv()

import os
porta = int(os.getenv("PORT"))


from os import listdir
from os.path import isfile, join

modules = listdir("Modules")
for module in modules:
    if isfile(join("Modules", module)):
        continue
    files = listdir(f"Modules/{module}/routers")
    for file in files:
        if file.endswith(".py"):
        
            exec(f"from Modules.{module}.routers import {file[:-3]}")

            
            exec(f"app.include_router({file[:-3]}.router)")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
