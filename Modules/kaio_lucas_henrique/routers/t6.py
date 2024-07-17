from fastapi import FastAPI, APIRouter
from scapy.all import rdpcap, TCP, IP, Raw
from scapy.layers.http import HTTPRequest
from pydantic import BaseModel
import threading
import uvicorn

app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/http", tags=["HTTP Analysis"])

class HTTPData(BaseModel):
    method: str
    host: str
    path: str
    status_code: int
    count: int = 1

http_data_storage = []

pcap_file_path = './pcaps/http.pcap'

def capture_http_data():
    packets = rdpcap(pcap_file_path)
    for packet in packets:
        if packet.haslayer(HTTPRequest):
            http_layer = packet[HTTPRequest]
            host = http_layer.Host.decode() if http_layer.Host else "Unknown Host"
            path = http_layer.Path.decode() if http_layer.Path else "/"
            method = http_layer.Method.decode() if http_layer.Method else "Unknown Method"
            status_code = int(packet[TCP].sport)  # Simplificação, deve ser adaptado
            # Armazenar dados
            http_data_storage.append(HTTPData(method=method, host=host, path=path, status_code=status_code))

@router.on_event("startup")
def start_http_capture():
    thread = threading.Thread(target=capture_http_data)
    thread.start()

@router.get("/http-requests", response_model=list[HTTPData])
def get_http_requests():
    return http_data_storage

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3002)
