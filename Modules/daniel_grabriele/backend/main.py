from fastapi import FastAPI, UploadFile, File
from typing import List, Dict
import dpkt
import io
from starlette.middleware.cors import CORSMiddleware
from collections import Counter
import requests
import uvicorn
from netaddr import EUI
import struct
from datetime import datetime, timedelta
import random 
from scapy.all import *

app = FastAPI()

# Configuração do middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista para armazenar os pacotes
pacotes = []

pacotes_udp_por_ip = {}
limite_pacotes_por_segundo = 100
ips_bloqueados = {}
pacotes_tcp = []

@app.get("/")
def read_root():
    return {"Hello world"}

@app.post("/ipv4/list_packages")
async def listar_pacotes_ipv4(pcap_file: UploadFile = File(...)):
    global pacotes
    pacotes = []
    conteudo = await pcap_file.read()
    captura = dpkt.pcapng.Reader(io.BytesIO(conteudo))

    for timestamp, buf in captura:
        # Decodificar o pacote Ethernet
        pacote_eth = dpkt.ethernet.Ethernet(buf)

        # Verificar se o pacote é do tipo IPv4
        if isinstance(pacote_eth.data, dpkt.ip.IP):
            ip = pacote_eth.data

            # Adicionar informações do pacote à lista
            pacotes.append({
                "timestamp": timestamp,
                "ip_origem": dpkt.utils.inet_to_str(ip.src),
                "ip_destino": dpkt.utils.inet_to_str(ip.dst),
                "versao": ip.v,
                "tamanho_cabecalho": ip.hl * 4,  # Tamanho do cabeçalho em bytes
                "tipo_servico": ip.tos,
                "comprimento_total": ip.len,
                "identificacao": ip.id,
                "flags": ip.off >> 13, 
                "deslocamento_fragmento": ip.off & dpkt.ip.IP_OFFMASK,
                "ttl": ip.ttl,
                "soma_verificacao": ip.sum,
                "protocolo": ip.p,
            })

    return {"mensagem": "Pacotes processados com sucesso", "pacotes": pacotes }

@app.get("/contar_ip/{endereco_ip}")
async def contar_ip(endereco_ip: str):
    global pacotes
    contador = Counter([pacote["ip_origem"] for pacote in pacotes])

    return {"endereco_ip": endereco_ip, "ocorrencias": contador[endereco_ip]}

@app.get("/listar_enderecos_ip")
async def listar_enderecos_ip():
    global pacotes

    # Extrair endereços IP únicos da lista de pacotes
    enderecos_ip_unicos = set(pacote["ip_origem"] for pacote in pacotes)

    return {"enderecos_ip": list(enderecos_ip_unicos)}

@app.post("/arp/list_packages")
async def listar_pacotes_arp(pcap_file: UploadFile = File(...)):
    global pacotes_arp
    pacotes_arp = []
    conteudo = await pcap_file.read()
    captura = dpkt.pcap.Reader(io.BytesIO(conteudo))

    for timestamp, buf in captura:
        # Decodificar o pacote Ethernet
        pacote_eth = dpkt.ethernet.Ethernet(buf)

        # Verificar se o pacote é do tipo ARP
        if isinstance(pacote_eth.data, dpkt.arp.ARP):
            arp = pacote_eth.data

            # Adicionar informações do pacote ARP à lista
            pacotes_arp.append({
                "timestamp": timestamp,
                "operation": arp.op,
                "sender_hardware_address": ":".join("{:02x}".format(b) for b in arp.sha),
                "sender_protocol_address": dpkt.utils.inet_to_str(arp.spa),
                "target_hardware_address": ":".join("{:02x}".format(b) for b in arp.tha),
                "target_protocol_address": dpkt.utils.inet_to_str(arp.tpa),
            })
            
    return {"mensagem": "Pacotes ARP processados com sucesso", "pacotes": pacotes_arp}

@app.post("/rip/listar_pacotes")
async def listar_pacotes_rip(pcap_file: UploadFile = File(...)):
    global pacotes_rip
    pacotes_rip = [] 
    conteudo = await pcap_file.read()
    captura = dpkt.pcap.Reader(io.BytesIO(conteudo))

    for timestamp, buf in captura:
        # Decodificar o pacote Ethernet
        pacote_eth = dpkt.ethernet.Ethernet(buf)

        # Verificar se o pacote é do tipo IP e UDP
        if isinstance(pacote_eth.data, dpkt.ip.IP) and isinstance(pacote_eth.data.data, dpkt.udp.UDP):
            ip = pacote_eth.data
            udp = ip.data

            # Verificar se é um pacote RIP
            if udp.dport == 520 or udp.sport == 520:
                rip = dpkt.rip.RIP(udp.data)

                # Interpretar o tipo de comando RIP
                tipo_comando = "Unknown"
                if rip.cmd == 1:
                    tipo_comando = "Request"
                elif rip.cmd == 2:
                    tipo_comando = "Response"

                # Processar as entradas RIP
                entries = []
                for entry in rip.data:
                    entries.append({
                        "address_family": entry.family,
                        "route_tag": entry.route_tag,
                        "ip_address": dpkt.utils.inet_to_str(entry.addr.to_bytes(4, 'big')),
                        "next_hop": dpkt.utils.inet_to_str(entry.next_hop.to_bytes(4, 'big')),
                        "metric": entry.metric,
                    })

                # Adicionar informações do pacote RIP à lista
                pacotes_rip.append({
                    "timestamp": timestamp,
                    "source_ip": dpkt.utils.inet_to_str(ip.src),
                    "destination_ip": dpkt.utils.inet_to_str(ip.dst),
                    "command_type": tipo_comando,
                    "version": rip.v,
                    "entries": entries,
                })

    return {"message": "Pacotes RIP processados com sucesso", "pacotes": pacotes_rip}
  
def detectar_anomalias(ip, udp):
    anomalias = []

    # Portas comuns UDP
    portas_comuns = {53, 67, 68, 123, 161, 162, 500, 514, 1812, 1813}

    # Porta incomum
    if udp.sport not in portas_comuns and udp.dport not in portas_comuns:
        anomalias.append("Porta incomum")
        registrar_ip_para_ddos(dpkt.utils.inet_to_str(ip.src))  # Registrar IP para DDoS

    # Comprimento inesperado
    if udp.ulen < 8 or udp.ulen > 512: 
        anomalias.append("Comprimento inesperado")
        registrar_ip_para_ddos(dpkt.utils.inet_to_str(ip.src)) 

    # Checksum inválido
    udp_pseudo_header = struct.pack('!4s4sBBH', ip.src, ip.dst, 0, dpkt.ip.IP_PROTO_UDP, udp.ulen)
    udp_data = udp_pseudo_header + bytes(udp)
    if calcular_checksum(udp_data) != 0:
        anomalias.append("Checksum inválido")
        registrar_ip_para_ddos(dpkt.utils.inet_to_str(ip.src))

    return anomalias

@app.post("/udp/list_packages")
async def listar_pacotes_udp(pcap_file: UploadFile = File(...)):
    global pacotes_udp
    pacotes_udp = []
    conteudo = await pcap_file.read()
    captura = dpkt.pcap.Reader(io.BytesIO(conteudo))

    for timestamp, buf in captura:
        # Decodificar o pacote Ethernet
        pacote_eth = dpkt.ethernet.Ethernet(buf)

        # Verificar se o pacote é do tipo IP e UDP
        if isinstance(pacote_eth.data, dpkt.ip.IP) and isinstance(pacote_eth.data.data, dpkt.udp.UDP):
            ip = pacote_eth.data
            udp = ip.data

            # Identificar protocolos específicos
            protocolo = "Desconhecido"
            porta_origem = udp.sport
            porta_destino = udp.dport

            # Identificação por portas conhecidas
            if porta_destino == 53:
                protocolo = "DNS"
            elif porta_destino == 123:
                protocolo = "NTP"
            elif porta_destino == 161:
                protocolo = "SNMP"
            elif porta_destino == 514:
                protocolo = "Syslog"
            elif porta_destino == 1900:
                protocolo = "SSDP"
            elif porta_destino == 389:
                protocolo = "CLDAP"
            
            # Verificar se o pacote é ICMP
            if isinstance(ip.data, dpkt.icmp.ICMP):
                protocolo = "ICMP"

            # Detectar anomalias
            anomalias = detectar_anomalias(ip, udp)

            # Adicionar informações do pacote UDP à lista
            pacotes_udp.append({
                "timestamp": timestamp,
                "ip_origem": dpkt.utils.inet_to_str(ip.src),
                "ip_destino": dpkt.utils.inet_to_str(ip.dst),
                "porta_origem": porta_origem,
                "porta_destino": porta_destino,
                "comprimento": udp.ulen,
                "checksum": udp.sum,
                "dados": udp.data.hex(),
                "protocolo": protocolo,
                "anomalias": anomalias
            })

             # Verificar e registrar o IP de origem para detecção de DDoS
            ip_origem = dpkt.utils.inet_to_str(ip.src)
            registrar_ip_para_ddos(ip_origem)
            
    return {"mensagem": "Pacotes UDP processados com sucesso", "pacotes": pacotes_udp}

def registrar_ip_para_ddos(ip_origem):
    global pacotes_udp_por_ip

    # Registrar o IP e a contagem de pacotes UDP
    if ip_origem in pacotes_udp_por_ip:
        pacotes_udp_por_ip[ip_origem]["count"] += 1
        pacotes_udp_por_ip[ip_origem]["last_seen"] = datetime.now()
    else:
        pacotes_udp_por_ip[ip_origem] = {
            "count": 1,
            "first_seen": datetime.now(),
            "last_seen": datetime.now()
        }

    # Verificar se o IP está gerando tráfego excessivo
    verificar_ddos(ip_origem)

def verificar_ddos(ip_origem):
    global pacotes_udp_por_ip, limite_pacotes_por_segundo

    # Verificar se o IP está na lista de pacotes UDP por IP
    if ip_origem in pacotes_udp_por_ip:
        # Calcular o tempo decorrido desde o primeiro e último pacote
        tempo_decorrido = (datetime.now() - pacotes_udp_por_ip[ip_origem]["first_seen"]).total_seconds()
        pacotes_por_segundo = pacotes_udp_por_ip[ip_origem]["count"] / tempo_decorrido

        # Verificar se a taxa de pacotes por segundo excede o limite
        if pacotes_por_segundo > limite_pacotes_por_segundo:
            # Verificar se o IP já está bloqueado
            if ip_origem in ips_bloqueados:
                # Verificar se o tempo de bloqueio já expirou
                if datetime.now() > ips_bloqueados[ip_origem]:
                    # Remover o IP da lista de bloqueados
                    del ips_bloqueados[ip_origem]
                else:
                    return  # IP ainda está bloqueado, não fazer nada
            else:
                # Bloquear o IP
                tempo_bloqueio = timedelta(seconds=3)
                tempo_desbloqueio = datetime.now() + tempo_bloqueio
                ips_bloqueados[ip_origem] = tempo_desbloqueio
                print(f"IP bloqueado por 5 minutos: {ip_origem}")

def calcular_checksum(data):
    if len(data) % 2 == 1:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word

    while (checksum >> 16) > 0:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum = ~checksum & 0xFFFF
    return checksum

@app.get("/ips_bloqueados")
async def get_ips_bloqueados():
    return {"ips_bloqueados": list(ips_bloqueados.keys())}

@app.post("/tcp/list_packages")
async def listar_pacotes_tcp(pcap_file: UploadFile = File(...), limite: int = 12000):
    pacotes_tcp = []
    conteudo = await pcap_file.read()
    captura = dpkt.pcap.Reader(io.BytesIO(conteudo))

    conexoes = {}

    for timestamp, buf in captura:
        # Decodificar o pacote Ethernet
        pacote_eth = dpkt.ethernet.Ethernet(buf)

        # Verificar se o pacote é do tipo IP e TCP
        if isinstance(pacote_eth.data, dpkt.ip.IP) and isinstance(pacote_eth.data.data, dpkt.tcp.TCP):
            ip = pacote_eth.data
            tcp = ip.data

            # Identificar flags TCP
            flags = []
            if tcp.flags & dpkt.tcp.TH_SYN:
                flags.append("SYN")
            if tcp.flags & dpkt.tcp.TH_ACK:
                flags.append("ACK")
            if tcp.flags & dpkt.tcp.TH_FIN:
                flags.append("FIN")
            if tcp.flags & dpkt.tcp.TH_RST:
                flags.append("RST")
            if tcp.flags & dpkt.tcp.TH_PUSH:
                flags.append("PSH")
            if tcp.flags & dpkt.tcp.TH_URG:
                flags.append("URG")

            # Adicionar informações do pacote TCP à lista
            pacotes_tcp.append({
                "timestamp": timestamp,
                "ip_origem": dpkt.utils.inet_to_str(ip.src),
                "ip_destino": dpkt.utils.inet_to_str(ip.dst),
                "porta_origem": tcp.sport,
                "porta_destino": tcp.dport,
                "flags": flags,
                "seq": tcp.seq,
                "ack": tcp.ack,
                "window_size": tcp.win,
                "checksum": tcp.sum,
                "dados": tcp.data.hex(),
                "tempo_resposta": 0.0
            })

            # Contar pacotes por conexão (IP de origem, IP de destino, porta de origem, porta de destino)
            conexao = f"{dpkt.utils.inet_to_str(ip.src)}:{tcp.sport} -> {dpkt.utils.inet_to_str(ip.dst)}:{tcp.dport}"
            if conexao not in conexoes:
                conexoes[conexao] = 0
            conexoes[conexao] += 1

            # Limitar o número de pacotes retornados
            if len(pacotes_tcp) >= limite:
                break

    # Calcular tempo de resposta (RTT) para pacotes SYN e ACK
    syn_ack_pairs = {}
    for pacote in pacotes_tcp:
        if "SYN" in pacote["flags"]:
            syn_ack_pairs[(pacote["ip_origem"], pacote["ip_destino"], pacote["porta_origem"], pacote["porta_destino"], pacote["seq"])] = pacote
        elif "ACK" in pacote["flags"]:
            key = (pacote["ip_destino"], pacote["ip_origem"], pacote["porta_destino"], pacote["porta_origem"], pacote["ack"] - 1)
            if key in syn_ack_pairs:
                syn_pacote = syn_ack_pairs[key]
                syn_timestamp = syn_pacote["timestamp"]
                ack_timestamp = pacote["timestamp"]
                syn_ack_pairs.pop(key)
                syn_pacote["tempo_resposta"] = ack_timestamp - syn_timestamp
                pacote["tempo_resposta"] = ack_timestamp - syn_timestamp

    return { "mensagem": "Pacotes TCP processados com sucesso", "pacotes": pacotes_tcp, "conexoes": conexoes }

@app.post("/dns/listar_pacotes")
async def listar_pacotes_dns(pcap_file: UploadFile = File(...)):
    pacotes_dns = []

    conteudo = await pcap_file.read()
    captura = dpkt.pcap.Reader(io.BytesIO(conteudo))

    def rdata_to_str(rdata: bytes) -> str:
        """Converte rdata para string, detectando se é um endereço IP."""
        if len(rdata) == 4:  # Assume que rdata com 4 bytes é um IP
            return dpkt.utils.inet_to_str(rdata)  # Converte bytes em IP
        return rdata.decode('utf-8', errors='ignore')  # Caso contrário, decodifica como string

    for timestamp, buf in captura:
        pacote_eth = dpkt.ethernet.Ethernet(buf)

        if isinstance(pacote_eth.data, dpkt.ip.IP):
            ip = pacote_eth.data

            if isinstance(ip.data, dpkt.udp.UDP) or isinstance(ip.data, dpkt.tcp.TCP):
                trans = ip.data

                if trans.dport == 53 or trans.sport == 53:
                    dns = dpkt.dns.DNS(trans.data)

                    queries = []
                    for query in dns.qd:
                        queries.append({
                            "name": query.name.decode('utf-8', errors='ignore') if isinstance(query.name, bytes) else query.name,
                            "type": query.type,
                            "class": query.cls
                        })

                    answers = []
                    for answer in dns.an:
                        rdata = rdata_to_str(answer.rdata)  # Converte rdata para string
                        answers.append({
                            "name": answer.name.decode('utf-8', errors='ignore') if isinstance(answer.name, bytes) else answer.name,
                            "type": answer.type,
                            "class": answer.cls,
                            "ttl": answer.ttl,
                            "rdata": rdata
                        })

                    # Determinar o tipo de servidor
                    server_type = []
                    if dns.qr == dpkt.dns.DNS_R:  # Resposta
                        if dns.op & dpkt.dns.DNS_AA:
                            server_type.append("Authoritative")
                        if dns.op & dpkt.dns.DNS_RA:
                            server_type.append("Recursive")
                    else:  # Solicitação
                        if dns.op & dpkt.dns.DNS_RD:
                            server_type.append("Recursion Desired")

                    pacotes_dns.append({
                        "timestamp": timestamp,
                        "source_ip": dpkt.utils.inet_to_str(ip.src),
                        "destination_ip": dpkt.utils.inet_to_str(ip.dst),
                        "queries": queries,
                        "answers": answers,
                        "opcode": dns.opcode,
                        "rcode": dns.rcode,
                        "id": dns.id,
                        "server_type": server_type
                    })

    return {"message": "Pacotes DNS processados com sucesso", "pacotes": pacotes_dns}

@app.post("/http/listar_pacotes")
async def listar_pacotes_http(pcap_file: UploadFile = File(...)):
    pacotes_http = []
    conteudo = await pcap_file.read()
    captura = dpkt.pcap.Reader(io.BytesIO(conteudo))

    for timestamp, buf in captura:
        pacote_eth = dpkt.ethernet.Ethernet(buf)
        if isinstance(pacote_eth.data, dpkt.ip.IP) and isinstance(pacote_eth.data.data, dpkt.tcp.TCP):
            ip = pacote_eth.data
            tcp = ip.data
            if tcp.dport == 80 or tcp.sport == 80 or tcp.dport == 8080 or tcp.sport == 8080:
                try:
                    http = dpkt.http.Request(tcp.data)
                    pacotes_http.append({
                        "timestamp": timestamp,
                        "ip_origem": dpkt.utils.inet_to_str(ip.src),
                        "ip_destino": dpkt.utils.inet_to_str(ip.dst),
                        "metodo": http.method,
                        "uri": http.uri,
                        "versao": http.version,
                        "headers": dict(http.headers),
                        "corpo": http.body.decode('utf-8', errors='ignore') if http.body else None,
                        "size": len(tcp.data)  # Tamanho da requisição HTTP
                    })
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                    pass

    return {"mensagem": "Pacotes HTTP processados com sucesso", "pacotes": pacotes_http}

@app.post("/snmp/listar_pacotes")
async def listar_pacotes_snmp(pcap_file: UploadFile = File(...)):
    pacotes_snmp = []

    # Lê o conteúdo do arquivo pcap
    conteudo = await pcap_file.read()

    # Analisa o arquivo pcap usando o Scapy
    pacotes = rdpcap(io.BytesIO(conteudo))

    for pacote in pacotes:
        # Verifica se é um pacote SNMP
        if SNMP in pacote:
            try:
                # Extrai informações relevantes do pacote SNMP
                pdu = pacote[SNMP].PDU
                pdu_type = pdu.__class__.__name__  # Obtém o nome da classe da PDU SNMP
                pacotes_snmp.append({
                    "timestamp": float(pacote.time),
                    "ip_origem": pacote[IP].src,
                    "ip_destino": pacote[IP].dst,
                    "versao": pacote[SNMP].version,
                    "comunidade": str(pacote[SNMP].community),  # Converte a comunidade SNMP para string
                    "comando": pdu_type,  # Tipo de PDU SNMP
                    # Adicione mais campos conforme necessário
                })
            except Exception as e:
                print(f"Erro ao processar pacote SNMP: {e}")

    return {"mensagem": "Pacotes SNMP processados com sucesso", "pacotes": pacotes_snmp}