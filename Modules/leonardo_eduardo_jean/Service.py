import os

from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.l2 import ARP
from scapy.layers.rip import RIP

from Modules.leonardo_eduardo_jean.Ipv4Packet import IPv4Packet
from Modules.leonardo_eduardo_jean.ArpPacket import ArpPacket
from Modules.leonardo_eduardo_jean.RipPacket import RipPacket


class Service:

    def read_ipv4_from_file(self):
        # Ler pacotes
        directory = os.path.dirname(os.path.abspath(__file__))
        packets = rdpcap(f"{directory}/../../pcaps/trabalho1.pcapng")

        # Limitar a quantidade de pacotes lidos para evitar utilização total da API de Geolocation
        packets = packets[:100]
        ipv4_packets = []

        for packet in packets:
            if IP in packet and packet[IP].version == 4:
                ip_packet = packet[IP]
                ipv4_packet = IPv4Packet(
                    version=ip_packet.version,
                    header_length=ip_packet.ihl,
                    service_type=ip_packet.tos,
                    total_length=ip_packet.len,
                    identification=ip_packet.id,
                    flags=ip_packet.flags,
                    frag_offset=ip_packet.frag,
                    ttl=ip_packet.ttl,
                    protocol=ip_packet.proto,
                    checksum=ip_packet.chksum,
                    src_ip=ip_packet.src,
                    dst_ip=ip_packet.dst,
                    options=ip_packet.options
                )
                ipv4_packets.append(ipv4_packet)

        return ipv4_packets

    def read_arp_from_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        pcap_path = f"{directory}/../../pcaps/trabalho2.pcap"

        packets = rdpcap(pcap_path)
        arp_packets = []

        for packet in packets:
            if ARP in packet:
                arp_packet = ArpPacket(
                    hardware_type=packet[ARP].hwtype,
                    protocol_type=packet[ARP].ptype,
                    hardware_src=packet[ARP].hwsrc,
                    protocol_src=packet[ARP].psrc,
                    hardware_dst=packet[ARP].hwdst,
                    protocol_dst=packet[ARP].pdst,
                    op=packet[ARP].op
                )
                arp_packets.append(arp_packet)

        return arp_packets

    def read_rip_from_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        pcap_path = f"{directory}/../../pcaps/trabalho3.pcap"

        packets = rdpcap(pcap_path)
        rip_packets = []

        for pkt in packets:
            rip_layer = pkt.getlayer(RIP)
            rip_payload = rip_layer.payload
            entry = RipPacket(rip_payload.AF, rip_payload.RouteTag, rip_payload.addr, rip_payload.mask, rip_payload.nextHop, rip_payload.metric, rip_payload.time)
            rip_packets.append(entry)

        return rip_packets




