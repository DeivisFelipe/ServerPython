from fastapi import APIRouter
from typing import Dict, List, Any, Tuple
import json
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, HTTPPacket, packetSource as src
from scapy.layers.http import HTTPResponse, HTTPRequest
from scapy.utils import rdpcap

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/http", tags=[""])


def parser_http_packet(packet, p_num) -> Tuple[Dict[str, Any], bool] | None:
    if packet.haslayer(HTTPRequest):
        http_layer = packet.getlayer(HTTPRequest)
        http_info = {
            'Packet Number': p_num,
            'Method': http_layer.Method.decode() if http_layer.Method else None,
            'Host': http_layer.Host.decode() if http_layer.Host else None,
            'Path': http_layer.Path.decode() if http_layer.Path else None,
            'User-Agent': http_layer.User_Agent.decode() if http_layer.User_Agent else None,
            'Referer': http_layer.Referer.decode() if http_layer.Referer else None,
            'Cookie': http_layer.Cookie.decode() if http_layer.Cookie else None,
            'Accept': http_layer.Accept.decode() if http_layer.Accept else None,
        }
        return http_info, True

    elif packet.haslayer(HTTPResponse):
        http_layer = packet.getlayer(HTTPResponse)
        http_info = {
            'Packet Number': p_num,
            'Status-Code': http_layer.Status_Code.decode() if http_layer.Status_Code else None,
            'Reason-Phrase': http_layer.Reason_Phrase.decode() if http_layer.Reason_Phrase else None,
            'Content-Type': http_layer.Content_Type.decode() if http_layer.Content_Type else None,
            'Content-Length': http_layer.Content_Length.decode() if http_layer.Content_Length else None,
            'Server': http_layer.Server.decode() if http_layer.Server else None,
        }
        return http_info, False

    return None


pcaplist = rdpcap("./pcaps/http_witp_jpegs.pcap")
httpResquestPackets: List[Any] = []
httpResponsePackets: List[Any] = []

count = 1
for pkt in pcaplist:
    http_pkt = parser_http_packet(pkt, count)
    count += 1
    if http_pkt:
        if http_pkt[1]:
            httpResquestPackets.append(http_pkt[0])
        else:
            httpResponsePackets.append(http_pkt[0])


@router.get("/info")
def test():
    x = httpResponsePackets
    y = httpResquestPackets
    
    resp = {"Responses": x, "Requests": y}
    return resp


@router.get("/methods")
def get_methods():
    '''
      Retorna os metodos usados e quantas vezes foram usados
      '''

    for packet in src.allPackets:
        if isinstance(packet, HTTPPacket):
            yield packet.isResponse
