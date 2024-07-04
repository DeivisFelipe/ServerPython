from fastapi import APIRouter
from typing import Dict, List, Any
import json
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, UDPPacket, IPPacket, TCPPacket, packetSource as src

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/http", tags=[""])


@router.get("/methods")
def get_methods():
    '''
    Retorna os metodos usados e quantas vezes foram usados
    '''

    for packet in src:
        if isinstance(packet, IPPacket):
            if packet.protocol == 6:
                if isinstance(packet.data, TCPPacket):
                    if packet.data.destination_port == 80:
                        return packet.data.method
    pass