import os

from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.l2 import ARP
from scapy.layers.rip import RIP
from scapy.layers.snmp import SNMP, SNMPnext
from collections import Counter
from collections import defaultdict

from Modules.leonardo_eduardo_jean.DnsPacket import DnsPacket
from Modules.leonardo_eduardo_jean.Ipv4Packet import IPv4Packet
from Modules.leonardo_eduardo_jean.ArpPacket import ArpPacket
from Modules.leonardo_eduardo_jean.RipPacket import RipPacket
from Modules.leonardo_eduardo_jean.TcpPacket import TcpPacket
from Modules.leonardo_eduardo_jean.UdpPacket import UdpPacket


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

        for packet in packets:
            rip_layer = packet.getlayer(RIP)
            rip_payload = rip_layer.payload
            entry = RipPacket(rip_payload.AF, rip_payload.RouteTag, rip_payload.addr, rip_payload.mask, rip_payload.nextHop, rip_payload.metric, rip_payload.time)
            rip_packets.append(entry)

        return rip_packets

    def read_udp_from_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        pcap_path = f"{directory}/../../pcaps/trabalho4.pcap"

        packets = rdpcap(pcap_path)
        udp_packets = []

        for packet in packets:
            if UDP in packet:
                packetEntry = packet[UDP]
                udp_packet = UdpPacket(packetEntry.sport, packetEntry.dport, packetEntry.len, packetEntry.chksum)
                udp_packets.append(udp_packet)
        return udp_packets

    def read_tcp_from_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        pcap_path = f"{directory}/../../pcaps/trabalho5.pcap"

        try:
            packets = rdpcap(pcap_path)
        except FileNotFoundError:
            print(f"Arquivo PCAP não encontrado em: {pcap_path}")
            return []
        except Scapy_Exception as e:
            print(f"Erro ao ler o arquivo PCAP: {e}")
            return []

        return packets

    def read_http_from_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        pcap_path = f"{directory}/../../pcaps/trabalho6.pcap"

        packets = rdpcap(pcap_path)
        http_verbs = []

        for packet in packets:
            if hasattr(packet.payload, 'load') and b'HTTP' in packet.payload.load:
                http_payload = packet.payload.load.decode('utf-8', errors='ignore')
                verb = http_payload.split()[0] if http_payload else None
                if verb in ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']:
                    http_verbs.append(verb)

        verb_counts = Counter(http_verbs)

        return verb_counts


    def read_dns_from_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        pcap_path = f"{directory}/../../pcaps/trabalho7.pcap"

        packets = rdpcap(pcap_path)
        dns_packets = []

        for packet in packets:
            if DNS in packet:
                dns_layer = packet[DNS]
                if dns_layer.qr == 0:  # Query
                    for i in range(dns_layer.qdcount):
                        query = dns_layer[DNSQR][i]
                        dns_packet = DnsPacket(
                            transaction_id=dns_layer.id,
                            query_name=query.qname.decode('utf-8'),
                            query_type=query.qtype,
                            query_class=query.qclass,
                            response_code=dns_layer.rcode
                        )
                        dns_packets.append(dns_packet)
                elif dns_layer.qr == 1:  # Response
                    for i in range(dns_layer.ancount):
                        answer = dns_layer.an[i]
                        dns_packet = DnsPacket(
                            transaction_id=dns_layer.id,
                            query_name=answer.rrname.decode('utf-8'),
                            query_type=answer.type,
                            query_class=answer.rclass,
                            response_code=dns_layer.rcode
                        )
                        dns_packets.append(dns_packet)
        return dns_packets

    def read_snmp_from_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        pcap_path = f"{directory}/../../pcaps/trabalho8.pcap"

        packets = rdpcap(pcap_path)
        pdu_counts = defaultdict(int)

        for packet in packets:
            if SNMP in packet or SNMPnext in packet:
                snmp_layer = packet[SNMP] if SNMP in packet else packet[SNMPnext]
                pdu_type = snmp_layer.PDU.name
                pdu_counts[pdu_type] += 1

        return dict(pdu_counts)