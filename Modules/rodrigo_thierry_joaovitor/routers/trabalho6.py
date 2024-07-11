from fastapi import APIRouter
from typing import Dict, List, Any
import json
from ...rodrigo_thierry_joaovitor.Parser import PacketSource, HTTPPacket, packetSource as src

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/http", tags=[""])


@router.get("/methods")
def get_methods():
    '''
    Retorna os metodos usados e quantas vezes foram usados
    '''

    for packet in src.allPackets:
        if isinstance(packet, HTTPPacket):
            yield packet.isResponse
    