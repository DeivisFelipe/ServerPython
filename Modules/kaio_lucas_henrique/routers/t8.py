from fastapi import FastAPI, APIRouter
from scapy.all import rdpcap, SNMP, SNMPget, SNMPset, SNMPresponse, SNMPnext
from scapy.layers.inet import IP
from pydantic import BaseModel
import threading
import uvicorn

app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/snmp", tags=["SNMP Analysis"])

class SNMPRequestData(BaseModel):
    device: str
    message_type: str
    count: int

snmp_data_storage = []

pcap_file_path = './pcaps/snmp.pcap'

def analyze_snmp_traffic():
    packets = rdpcap(pcap_file_path)
    snmp_requests = {}
    for packet in packets:
        if packet.haslayer(SNMP):
            snmp_layer = packet[SNMP]
            device = packet[IP].dst  
            if SNMPget in packet:
                message_type = "GET"
            elif SNMPset in packet:
                message_type = "SET"
            elif SNMPresponse in packet:
                message_type = "RESPONSE"
            elif SNMPnext in packet:
                message_type = "NEXT"
            else:
                message_type = "OTHER"
            request_key = (device, message_type)
            if request_key in snmp_requests:
                snmp_requests[request_key]['count'] += 1
            else:
                snmp_requests[request_key] = {
                    'device': device,
                    'message_type': message_type,
                    'count': 1
                }
    for key, value in snmp_requests.items():
        snmp_data_storage.append(SNMPRequestData(**value))

@router.on_event("startup")
def start_snmp_analysis():
    thread = threading.Thread(target=analyze_snmp_traffic)
    thread.start()

@router.get("/snmp-requests", response_model=list[SNMPRequestData])
def get_snmp_requests():
    return snmp_data_storage

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
