from fastapi import FastAPI, APIRouter
from scapy.all import rdpcap, TCP, IP
from pydantic import BaseModel
import threading
import requests
import uvicorn

app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/tcp", tags=["Analysis"])

class ConnectionData(BaseModel):
    source_ip: str
    source_location: str
    destination_ip: str
    destination_location: str

geo_data_storage = []

pcap_file_path = './pcaps/tcp.pcap'

def get_location(ip):
    response = requests.get(f'https://ipapi.co/{ip}/json/')
    data = response.json()
    return f"{data['city']}, {data['country_name']}"

def capture_tcp_geo_data():
    packets = rdpcap(pcap_file_path)
    for packet in packets:
        if IP in packet and TCP in packet:
            source_location = get_location(packet[IP].src)
            destination_location = get_location(packet[IP].dst)
            connection = {
                'source_ip': packet[IP].src,
                'source_location': source_location,
                'destination_ip': packet[IP].dst,
                'destination_location': destination_location
            }
            geo_data_storage.append(connection)

@router.on_event("startup")
def start_tcp_geo_capture():
    thread = threading.Thread(target=capture_tcp_geo_data)
    thread.start()

@router.get("/connection-data", response_model=list[ConnectionData])
def get_connection_data():
    return geo_data_storage

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
