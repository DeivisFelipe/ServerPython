from fastapi import FastAPI, APIRouter
from scapy.all import rdpcap, SNMP, SNMPvarbind
from pydantic import BaseModel
import threading
import uvicorn

app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/snmp", tags=["SNMP Analysis"])

class SNMPData(BaseModel):
    operation: str
    response_time: float
    error_status: int

snmp_data_storage = []

pcap_file_path = './pcaps/snmp.pcap'

def analyze_snmp_traffic():
    packets = rdpcap(pcap_file_path)
    start_times = {}
    for packet in packets:
        if SNMP in packet:
            try:
                pdu = packet[SNMP]
                if pdu.PDU in [0, 1, 3]:  # GET, GET-NEXT, SET
                    operation = {0: 'GET', 1: 'GET-NEXT', 3: 'SET'}[pdu.PDU]
                    request_id = pdu.id
                    start_times[request_id] = packet.time
                elif pdu.PDU == 2:  # RESPONSE
                    request_id = pdu.id
                    if request_id in start_times:
                        response_time = packet.time - start_times[request_id]
                        error_status = pdu.error
                        snmp_data_storage.append(SNMPData(operation='RESPONSE', response_time=response_time, error_status=error_status))
            except AttributeError as e:
                print(f"Error processing packet: {e}")

@router.on_event("startup")
def start_snmp_analysis():
    thread = threading.Thread(target=analyze_snmp_traffic)
    thread.start()

@router.get("/snmp-data", response_model=list[SNMPData])
def get_snmp_data():
    return snmp_data_storage

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
