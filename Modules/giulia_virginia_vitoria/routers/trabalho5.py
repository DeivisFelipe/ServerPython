import dpkt
from collections import defaultdict, Counter
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import shutil
import os

router = APIRouter()
app = FastAPI()

# Classe para representar as informações dos pacotes
class PacketInfo(BaseModel):
    flows: int
    total_bytes: int
    flags: dict

def count_tcp_flows(pcap_file):
    flows = defaultdict(int)
    bytes_per_flow = 0  # Variável para armazenar bytes por fluxo
    flags_counter = Counter()
    
    # Contar o número de fluxos em um arquivo pcap usando handshake do TCP
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue
            ip = eth.data
            if ip.p != dpkt.ip.IP_PROTO_TCP:
                continue
            tcp = ip.data
            flow_key = (ip.src, tcp.sport, ip.dst, tcp.dport)
            if tcp.flags & dpkt.tcp.TH_SYN and not tcp.flags & dpkt.tcp.TH_ACK:
                flows[flow_key] += 1
            if tcp.flags & dpkt.tcp.TH_ACK:
                flows[(ip.dst, tcp.dport, ip.src, tcp.sport)] += 1

            # Acumular bytes por fluxo
            bytes_per_flow += len(tcp)
            
            if tcp.flags & dpkt.tcp.TH_SYN:
                flags_counter['SYN'] += 1
            if tcp.flags & dpkt.tcp.TH_ACK:
                flags_counter['ACK'] += 1
            if tcp.flags & dpkt.tcp.TH_FIN:
                flags_counter['FIN'] += 1
            if tcp.flags & dpkt.tcp.TH_RST:
                flags_counter['RST'] += 1
            if tcp.flags & dpkt.tcp.TH_PUSH:
                flags_counter['PSH'] += 1
            if tcp.flags & dpkt.tcp.TH_URG:
                flags_counter['URG'] += 1
            if tcp.flags & dpkt.tcp.TH_ECE:
                flags_counter['ECE'] += 1
            if tcp.flags & dpkt.tcp.TH_CWR:
                flags_counter['CWR'] += 1

    return len(flows), bytes_per_flow, flags_counter

@router.get("/trabalho5", response_model=PacketInfo)
async def count_flows():
    pcap_file = './pcaps/trabalho5.pcap'
    flows, bytes_per_flow, flags_counter = count_tcp_flows(pcap_file)

    result = {
        "flows": flows,
        "total_bytes": bytes_per_flow,
        "flags": dict(flags_counter)
    }
    return result

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)
