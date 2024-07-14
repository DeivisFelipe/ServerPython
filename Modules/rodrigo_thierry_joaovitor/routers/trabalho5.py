from fastapi import APIRouter
from typing import Dict, List, Any
import json
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, UDPPacket, IPPacket, TCPPacket
from ...rodrigo_thierry_joaovitor.PortFinder import findService

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/tcp", tags=[""])
src_allPackets, src_allPacketsDict = PacketSource.read("tcp.pcap")


@router.get("/conversations")
def get_conversations():
    TCP_pkts: List[IPPacket] = src_allPacketsDict[IPPacket]

    set_tcp: set[tuple[str, str]] = set()

    for pkt in TCP_pkts:
        if (pkt.protocol == "TCP"):
            tmp: List[str, str] = [pkt.sourceIp, pkt.destinationIp]
            tmp.sort()

            set_tcp.add(tuple(tmp))

    return sorted(set_tcp)


count_src = count_dst = 0


@router.get("/info/{src_ip}/{src_port}/{dst_ip}/{dst_port}")
def get_tcp_info(src_ip: str, src_port: int, dst_ip: str, dst_port: int):
    TCP_pkts: List[TCPPacket] = src_allPacketsDict[TCPPacket]

    src_ip = src_ip.strip()
    dst_ip = dst_ip.strip()

    infos: Dict[Any, Any] = dict()

    infos[src_ip] = dict()
    infos[dst_ip] = dict()
    infos[src_ip]["n_pkt"] = 0
    infos[src_ip]["w_size"] = []
    infos[src_ip]["timestamp"] = []
    infos[src_ip]["payload_size"] = []
    infos[src_ip]["bind"] = []
    infos[dst_ip]["n_pkt"] = 0
    infos[dst_ip]["w_size"] = []
    infos[dst_ip]["timestamp"] = []
    infos[dst_ip]["bind"] = []
    infos[dst_ip]["payload_size"] = []

    for pkt in TCP_pkts:

        if src_ip == pkt.external_pdu.sourceIp and dst_ip == pkt.external_pdu.destinationIp:
            infos[src_ip]["n_pkt"] += 1
            infos[src_ip]["w_size"].append(pkt.window)
            infos[src_ip]["timestamp"].append(pkt.ts)
            infos[src_ip]["bind"].append((pkt.srcPort, pkt.dstPort))

            ip_pkt: IPPacket = pkt.external_pdu
            infos[src_ip]["payload_size"].append(ip_pkt.length - (pkt.data_offset + ip_pkt.headerLength))

        elif dst_ip == pkt.external_pdu.sourceIp and src_ip == pkt.external_pdu.destinationIp:
            infos[dst_ip]["n_pkt"] += 1
            infos[dst_ip]["w_size"].append(pkt.window)
            infos[dst_ip]["timestamp"].append(pkt.ts)
            infos[dst_ip]["bind"].append((pkt.srcPort, pkt.dstPort))

            ip_pktd: IPPacket = pkt.external_pdu
            infos[dst_ip]["payload_size"].append(ip_pktd.length - (pkt.data_offset + ip_pktd.headerLength)*4)

    return infos
