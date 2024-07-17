from scapy.all import rdpcap, SNMP
import json  # Adicionando a importação do módulo json
from collections import defaultdict

def analyze_snmp_responses(pcap_file):
    packets = rdpcap(pcap_file)
    responses = {}

    for packet in packets:
        if packet.haslayer(SNMP):
            snmp_layer = packet.getlayer(SNMP)
            if hasattr(snmp_layer, 'PDU'):
                pdu_type = snmp_layer.PDU.__class__.__name__
                if pdu_type == 'SNMPresponse':
                    timestamp = int(packet.time)
                    if timestamp in responses:
                        responses[timestamp] += 1
                    else:
                        responses[timestamp] = 1

    # Transformar os dados em uma lista ordenada por tempo
    response_data = [{'timestamp': ts, 'count': count} for ts, count in sorted(responses.items())]

    return response_data

def main():
    pcap_file = 'snmp.pcap'
    response_data = analyze_snmp_responses(pcap_file)

    # Gerando o JSON para Echarts.js
    with open('echarts_response_data.json', 'w') as f:
        json.dump(response_data, f, indent=4)

    print("JSON gerado com sucesso para Echarts.js.")

if __name__ == "__main__":
    main()
