import requests
from scapy.layers.inet import TCP


def FilterIpv4(packets):
    report = {"localizacao": [], "ips": []}
    public_src_ips = 0
    public_dst_ips = 0
    private_src_ips = 0
    private_dst_ips = 0

    # Montar relatório
    for packet in packets:
        if packet.get_has_any_public_ip():
            objeto = {
                "ipOrigem": packet.get_origin_location(),
                "ipDestino": packet.get_destiny_location()
            }
            report["localizacao"].append(objeto)

            if packet.get_has_origin_public_ip():
                public_src_ips += 1
            else:
                private_src_ips +=1

            if packet.get_has_destiny_public_ip():
                public_dst_ips += 1
            else:
                private_dst_ips += 1
        else:
            private_dst_ips += 1
            private_src_ips += 1

    report["ips"].append({"tipo": "IP origem público", "quantidade": public_src_ips})
    report["ips"].append({"tipo": "IP destino público", "quantidade": public_dst_ips})
    report["ips"].append({"tipo": "IP origem privado", "quantidade": private_src_ips})
    report["ips"].append({"tipo": "IP destino privado", "quantidade": private_dst_ips})

    return report

def FilterARP(packets):
    report = []
    macAdressList = []

    for packet in packets:
        if packet.hardware_src not in macAdressList:
            macAdressList.append(packet.hardware_src)
        if packet.hardware_dst not in macAdressList:
            macAdressList.append(packet.hardware_dst)


    for macAdress in macAdressList:
        url = f"https://api.macvendors.com/{macAdress}"

        response = requests.get(url)

        if response.status_code == 200:
            vendor = response.text
            found = False

            for item in report:
                if item['fabricante'] == vendor:
                    item['quantidade'] += 1
                    found = True
                    break

            if not found:
                report.append({"fabricante": vendor, "quantidade": 1})

    return report


def FilterTCP(packets):
    report = {
        "window_sizes": [],
        "timestamps": []
    }

    for packet in packets:
        if TCP in packet:
            report["window_sizes"].append(packet[TCP].window)
            report["timestamps"].append(float(packet.time))

    return report



