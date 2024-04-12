from fastapi import APIRouter
from Modules.leonardo_eduardo_jean.Service import Service
from Modules.leonardo_eduardo_jean.Filter import FilterIpv4, FilterARP

router = APIRouter(prefix="/leonardo_eduardo_jean", tags=[""])

service = Service()

@router.get("/ipv4")
async def get_ip_location():
    packets = service.read_ipv4_from_file()
    report = FilterIpv4(packets)
    return report

@router.get("/arp")
async def get_ip_location():
    packets = service.read_arp_from_file()
    report = FilterARP(packets)
    return report

