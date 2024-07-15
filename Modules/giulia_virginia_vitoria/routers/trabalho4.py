import dpkt
from collections import defaultdict
from fastapi import FastAPI
from manuf import manuf
from fastapi import APIRouter
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
router = APIRouter()
pcap_file_path = './pcaps/trabalho4.pcap'

app = FastAPI()
parser = manuf.MacParser()
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
    443: "HTTPS"
    514: "Syslog",
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


@router.get("/trabalho4-1")
async def root():
    #Return UDP data from pcap file
    with open(pcap_file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        # Dicionário para armazenar o número de pacotes por segundo
        packet_counts = defaultdict(int)
        # Dicionário para armazenar o total de bytes por segundo
        byte_counts = defaultdict(int)
        # Dicionário para armazenar os serviços detectados
        service_counts = defaultdict(int)

        for timestamp, buf in pcap:
            # Analisar o quadro Ethernet
            eth = dpkt.ethernet.Ethernet(buf)
            # Verificar se os dados do Ethernet contêm um pacote IP
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                # Verificar se o pacote é um pacote UDP
                if isinstance(ip.data, dpkt.udp.UDP):
                    udp = ip.data
                    # Obter as portas de origem e destino
                    src_port = udp.sport
                    dst_port = udp.dport
                    # Incrementar a contagem de pacotes e bytes por segundo
                    ts_sec = int(timestamp)
                    packet_counts[ts_sec] += 1
                    byte_counts[ts_sec] += len(buf)
                    # Obter os serviços associados às portas de origem e destino
                    src_service = get_service(src_port)
                    dst_service = get_service(dst_port)
                    service_counts[src_service] += 1
                    service_counts[dst_service] += 1
    
    # Ordenar os timestamps
    sorted_timestamps = sorted(packet_counts.keys())
    # Extrair as contagens em ordem ordenada
    packets_per_second = [packet_counts[ts] for ts in sorted_timestamps]
    bytes_per_second = [byte_counts[ts] for ts in sorted_timestamps]
    

    response = {
        "packets_per_second": packets_per_second,
        "bytes_per_second": bytes_per_second,
        "service_counts": service_counts
    }
    return response

def get_service(port):
    return known_ports.get(port, "Unknown")


@router.get("/trabalho4-2")
async def get_vendor_data():
    response = defaultdict(int)

    with open(pcap_file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                src_mac = eth.src.hex()
                dst_mac = eth.dst.hex()

                src_vendor = parser.get_manuf(src_mac)
                dst_vendor = parser.get_manuf(dst_mac)
                #pega o nome do fabricante do dispositivo
                response[src_vendor] += 1
                response[dst_vendor] += 1
    return response

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3001)