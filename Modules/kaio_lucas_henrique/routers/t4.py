from fastapi import FastAPI, APIRouter
from scapy.all import rdpcap, UDP, IP  # Importando a camada IP
from pydantic import BaseModel
import threading
import uvicorn

# Inicializa o FastAPI
app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/udp", tags=["Analysis"])

class UDPData(BaseModel):
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    length: int

udp_data_storage = []


pcap_file_path = './pcaps/udp.pcap'

def capture_udp_packets():
    packets = rdpcap(pcap_file_path)
    for packet in packets:
        if IP in packet and UDP in packet:  
            udp_data = {
                'source_ip': packet[IP].src,
                'destination_ip': packet[IP].dst,
                'source_port': packet[UDP].sport,
                'destination_port': packet[UDP].dport,
                'length': packet[UDP].len
            }
            udp_data_storage.append(udp_data)
    return udp_data_storage

@router.on_event("startup")
def start_udp_capture():
    thread = threading.Thread(target=capture_udp_packets)
    thread.start()

@router.get("/udp-data", response_model=list[UDPData])
def get_udp_data():
    return udp_data_storage


app.include_router(router)


from dotenv import load_dotenv
load_dotenv()

import os
port = int(os.getenv("PORT", 3001))


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
    uvicorn.run(app, host="127.0.0.1", port=port)
