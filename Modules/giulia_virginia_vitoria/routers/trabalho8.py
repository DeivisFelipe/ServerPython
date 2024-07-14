import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from scapy.all import rdpcap, IP, conf
from typing import List

router = APIRouter()
app = FastAPI()

class PacketInfo(BaseModel):
    number: int
    time: float
    source: str
    destination: str
    protocol: str
    length: int
    info: str

def protocol_number_to_name(proto_num):
    return conf.l2types.get(proto_num, str(proto_num))

def extract_packet_info(pcap_file):
    packets = rdpcap(pcap_file)
    packet_info_list = []

    for i, pkt in enumerate(packets):
        if IP in pkt:
            packet_info = PacketInfo(
                number=i + 1,
                time=pkt.time,
                source=pkt[IP].src,
                destination=pkt[IP].dst,
                protocol=protocol_number_to_name(pkt[IP].proto),
                length=len(pkt),
                info=pkt.summary()
            )
            packet_info_list.append(packet_info)

    print(f"Extracted {len(packet_info_list)} packets")
    return packet_info_list

# Caminho para o arquivo pcap (assumindo que você tem um arquivo pcap)
pcap_file_path = './pcaps/trabalho8.pcap'

# Chama a função extract_packet_info com o arquivo pcap desejado
packet_info_list = extract_packet_info(pcap_file_path)

@router.get("/trabalho8", response_model=List[PacketInfo])
def read_trabalho3():
    global packet_info_list
    return packet_info_list

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)