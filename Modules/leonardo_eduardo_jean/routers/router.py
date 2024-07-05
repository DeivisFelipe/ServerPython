from fastapi import APIRouter
from Modules.leonardo_eduardo_jean.Service import Service
from Modules.leonardo_eduardo_jean.Filter import FilterIpv4, FilterARP

router = APIRouter(prefix="/leonardo_eduardo_jean", tags=[""])

service = Service()

@router.get("/ipv4")
async def get_ipv4_packet():
    packets = service.read_ipv4_from_file()
    report = FilterIpv4(packets)
    return report

@router.get("/arp")
async def get_arp_packet():
    packets = service.read_arp_from_file()
    report = FilterARP(packets)
    return report

@router.get("/rip")
async def get_rip_packet():
    packets = service.read_rip_from_file()
    return packets

@router.get("/udp")
async def get_udp_packet():
    packets = service.read_udp_from_file()
    return packets

@router.get("/tcp")
async def get_tcp_packet():
    packets = service.read_tcp_from_file()
    return packets

@router.get("/http")
async def get_http_packet():
    packets = service.read_http_from_file()
    return packets

@router.get("/dns")
async def get_dns_packet():
    packets = service.read_dns_from_file()
    return packets

@router.get("/snmp")
async def get_snmp_packet():
    packets = service.read_snmp_from_file()
    return packets