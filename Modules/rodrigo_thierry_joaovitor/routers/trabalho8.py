from fastapi import APIRouter
from typing import Dict, List, Any
from scapy.all import rdpcap, SNMP
import json
from ...rodrigo_thierry_joaovitor.Parser import packetSource as src

router = APIRouter(prefix="/grupo_rodrigo_thierry_joao/snmp", tags=[""])

# vamo ler o pcap separado pq dpkt n suporta snmp

snmpPackets = rdpcap("./pcaps/snmp.pcap")


def parse_snmp_packet(packet) -> Dict[str, Any]:
    """
    Parse an SNMP packet and extract relevant information.
    """
    mib_entry = {}
    
    if packet.haslayer(SNMP):
        snmp = packet.getlayer(SNMP)
        # Extract information from the SNMP layer
        for var_bind in snmp.PDU.varbindlist:
            oid = var_bind.oid.val
            value = var_bind.value
            mib_entry[oid] = value

    
    return mib_entry

def build_tree(entries):
        tree = {}
        for oid in entries:
            oid_parts = oid.split(".")
            current = tree
            for part in oid_parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current["value"] = entries[oid]
        return tree

@router.get("/mib")
def get_mib():
    '''
    Retorna a tabela mib
    '''
    entries = {}

    for packet in snmpPackets:
        mib_entry = parse_snmp_packet(packet)
        if mib_entry:
            entries.update(mib_entry)

    # transformar a lista de oids em uma arvore recursiva
    mib = build_tree(entries)
    return mib

def build_tree_oids(oids: List[str]):
    tree = {}
    for oid in oids:
        oid_parts = oid.split(".")
        current = tree
        for part in oid_parts:
            if part not in current:
                current[part] = {}
            current = current[part]
        # current["value"] = None
    return tree

@router.get("/tree")
def get_tree():
    '''
    Retorna a tabela mib sem os valores. Scapy n consegue ler eles pelo visto
    '''
    oids = []

    for packet in snmpPackets:
        mib_entry = parse_snmp_packet(packet)
        if mib_entry:
            for oid in mib_entry:
                if oid not in oids:
                    oids.append(oid)

    # transformar a lista de oids em uma arvore recursiva
    mib = build_tree_oids(oids)
    return mib

@router.get("/oids")
def get_oids():
    '''
    Retorna os OIDs usados e quantas vezes foram usados
    '''
    oids = []

    for packet in snmpPackets:
        mib_entry = parse_snmp_packet(packet)
        if mib_entry:
            for oid in mib_entry:
                if oid not in oids:
                    oids.append(oid)
    return oids