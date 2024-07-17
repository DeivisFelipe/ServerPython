from fastapi import APIRouter
from typing import Dict, List, Any
from scapy.all import rdpcap, DNS
import json

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/dns", tags=[""])

rawpacket = rdpcap("./pcaps/dns.pcap")
packets: List[DNS] = []
for p in rawpacket:
    if p.haslayer(DNS):
        packets.append(p.getlayer(DNS))


def packet_to_dict(packet: DNS) -> Dict[str, Any]:
    ## check if is request or response.
    # read request url or response ip
    print(packet.id)
    if packet.qr == 0:
        return {
            "type": "request",
            "id": packet.id,
            "url": packet.qd.qname.decode("utf-8")
        }
    else:
        return {
            "type": "response",
            "ip": packet.an.rdata,
            "id": packet.id,
            "url": packet.qd.qname.decode("utf-8")
        }

@router.get("/pktCount")
def get_pkt_count() -> Dict[str, Any]:
    return {"count": len(packets)}

# mt grande pra ir tudo junto
@router.get("/packets/{start}/{end}")
def get_packets(start: int, end: int) -> List[Dict[str, Any]]:
    return [packet_to_dict(packet) for packet in packets[start:end]]

@router.get("/resolved")
def get_resolved() -> List[Dict[str, str]]:
    #return an array of keypairs with the resolved ips and its domain name
    # remove duplicates
    resolved = {}
    for packet in packets:
        if packet.qr == 1:
            resolved[packet.an.rdata] = packet.qd.qname.decode("utf-8")
    return [{"ip": ip, "domain": resolved[ip]} for ip in resolved]

@router.get("/senders")
def get_senders() -> List[str]:
    #return an array of unique senders
    senders = set()
    for packet in rawpacket:
        # get ip layer
        ip = packet.getlayer("IP")
        senders.add(ip.src)
    return list(senders)

@router.get("/receivers")
def get_receivers() -> List[str]:
    #return an array of unique receivers
    receivers = set()
    for packet in rawpacket:
        # get ip layer
        ip = packet.getlayer("IP")
        receivers.add(ip.dst)
    return list(receivers)

@router.get("/sender/{sender}")
def get_sender(sender: str):
    for packet in rawpacket:
        # get ip layer
        ip = packet.getlayer("IP")
        if ip.src == sender:
            yield packet_to_dict(packet.getlayer(DNS))