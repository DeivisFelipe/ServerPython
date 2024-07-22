import dpkt
from collections import defaultdict
from fastapi import FastAPI, APIRouter
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Configuração do FastAPI
app = FastAPI()
router = APIRouter()

# Arquivo PCAP
pcap_file_path = './pcaps/trabalho4.pcap'

# Dicionário de portas conhecidas
known_ports = {
    7: "Echo",
    9: "Discard",
    11: "Users",
    37: "Time",
    49: "TACACS",
    20: "FTP (Data)",
    21: "FTP (Control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP (Server)",
    68: "DHCP (Client)",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP Trap",
    194: "IRC",
    443: "HTTPS",
    514: "syslog",
    520: "RIP",
    587: "SMTP (Submission)",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP (Alternative)",
    9092: "Apache Kafka",
    27017: "MongoDB"
}

# Função para obter o serviço com base na porta
def get_service(port):
    return known_ports.get(port, "Unknown")

# Endpoint para retornar dados UDP do arquivo PCAP
@router.get("/trabalho4-1")
async def get_udp_data():
    with open(pcap_file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        # Dicionários para armazenar contagens de pacotes e bytes por segundo e serviços detectados
        packet_counts = defaultdict(int)
        byte_counts = defaultdict(int)
        service_counts = defaultdict(int)

        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if isinstance(ip.data, dpkt.udp.UDP):
                    udp = ip.data
                    src_port = udp.sport
                    dst_port = udp.dport
                    ts_sec = int(timestamp)
                    packet_counts[ts_sec] += 1
                    byte_counts[ts_sec] += len(buf)
                    src_service = get_service(src_port)
                    dst_service = get_service(dst_port)
                    service_counts[src_service] += 1
                    service_counts[dst_service] += 1
    
    sorted_timestamps = sorted(packet_counts.keys())
    packets_per_second = [packet_counts[ts] for ts in sorted_timestamps]
    bytes_per_second = [byte_counts[ts] for ts in sorted_timestamps]

    response = {
        "packets_per_second": packets_per_second,
        "bytes_per_second": bytes_per_second,
        "service_counts": service_counts
    }
    return response

# Endpoint para obter dados de fabricantes dos dispositivos
@router.get("/trabalho4-2")
async def get_mac_addresses():
    response = defaultdict(int)

    with open(pcap_file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                src_mac = eth.src.hex()
                dst_mac = eth.dst.hex()
                response[src_mac] += 1
                response[dst_mac] += 1
                
    return response

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)
