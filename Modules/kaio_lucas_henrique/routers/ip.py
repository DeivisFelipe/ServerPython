from fastapi import FastAPI, APIRouter
import uvicorn
from scapy.all import IP, rdpcap

app = FastAPI()
router = APIRouter(prefix="/kaio_lucas_henrique/ip", tags=["Analysis"])

class IPData:
    def __init__(self, timestamp, src_ip, dst_ip, ttl, proto, length):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ttl = ttl
        self.proto = proto
        self.length = length

def extract_ip_info(pcap_file):
    packets = rdpcap(pcap_file)
    ip_packets = []
    for pkt in packets:
        if IP in pkt:
            ip_packet = pkt[IP]
            info = IPData(
                timestamp=pkt.time,
                src_ip=ip_packet.src,
                dst_ip=ip_packet.dst,
                ttl=ip_packet.ttl,
                proto=ip_packet.proto,
                length=ip_packet.len
            )
            ip_packets.append(info)
    return ip_packets


pcap_file_path = './pcaps/trabalho1.pcapng'
ip_packets = extract_ip_info(pcap_file_path)

@router.get("/packets-sizes-comparasion")
def get_packet_sizes_comparasion():
    if len(ip_packets) == 0:
        return {"error": "No packets captured yet"}
    sizes = [ip.length for ip in ip_packets]
    average = sum(sizes) / len(sizes)
    max_size = max(sizes)
    min_size = min(sizes)
    above_average = [size for size in sizes if size > average]
    below_average = [size for size in sizes if size < average]
    return {
        "max_size": max_size,
        "min_size": min_size,
        "average_size": average,
        "difference_max_min": max_size - min_size,
        "count_above_average": len(above_average),
        "count_below_average": len(below_average),
        "percentage_above_average": (len(above_average) / len(sizes)) * 100,
        "percentage_below_average": (len(below_average) / len(sizes)) * 100
    }

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
