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