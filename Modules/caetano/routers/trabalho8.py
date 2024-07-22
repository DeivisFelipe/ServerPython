import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from scapy.all import rdpcap, IP, UDP, SNMP, SNMPnext
from typing import List
from collections import defaultdict
router = APIRouter()
app = FastAPI()


def extract_snmp_data(file_location):
    packets = rdpcap(file_location)
    pdu_counts = defaultdict(int)
    for packet in packets:
        if SNMP in packet or SNMPnext in packet:
            snmp_layer = packet[SNMP] if SNMP in packet else packet[SNMPnext]
            pdu_type = snmp_layer.PDU.name
            pdu_counts[pdu_type] += 1
    return pdu_counts
pcap_file_path = './pcaps/trabalho8.pcap'

# Chama a função extract_packet_info com o arquivo pcap desejado
packet_info_list = extract_snmp_data(pcap_file_path)

@router.get("/trabalho8")
def read_trabalho3():
    global packet_info_list
    return packet_info_list

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)