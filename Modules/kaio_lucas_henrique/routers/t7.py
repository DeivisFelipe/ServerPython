from fastapi import FastAPI, APIRouter
from scapy.all import rdpcap, DNS, DNSQR
from scapy.layers.dns import dnsqtypes
from pydantic import BaseModel
import threading
import uvicorn

app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/dns", tags=["DNS Analysis"])

class DNSQueryData(BaseModel):
    domain: str
    query_type: str
    count: int

dns_data_storage = []

pcap_file_path = './pcaps/dns.pcap'

def capture_dns_data():
    packets = rdpcap(pcap_file_path)
    query_count = {}
    for packet in packets:
        if packet.haslayer(DNS) and packet.haslayer(DNSQR):
            dns_query = packet[DNSQR]
            domain = dns_query.qname.decode().strip('.')
            query_type = dnsqtypes.get(dns_query.qtype, 'Unknown')
            key = (domain, query_type)
            if key in query_count:
                query_count[key] += 1
            else:
                query_count[key] = 1

    for (domain, query_type), count in query_count.items():
        dns_data_storage.append(DNSQueryData(domain=domain, query_type=query_type, count=count))

@router.on_event("startup")
def start_dns_capture():
    thread = threading.Thread(target=capture_dns_data)
    thread.start()

@router.get("/dns-queries", response_model=list[DNSQueryData])
def get_dns_queries():
    return dns_data_storage

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
