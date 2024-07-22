from scapy.all import *
from collections import defaultdict
from fastapi import FastAPI
from collections import Counter
import numpy as np

from scapy.layers.inet import IP
from scapy.layers.l2 import ARP
from scapy.layers.rip import RIP
from scapy.layers.inet import UDP
from scapy.layers.inet import TCP
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.dns import DNSQR
from scapy.layers.snmp import SNMP



app = FastAPI()



# IPV4

arquivo_pcapng = "./Data/ip.pcapng"
pacotes = rdpcap(arquivo_pcapng)
hosts = {}

contador_origem = defaultdict(int)
contador_destino = defaultdict(int)

for pacote in pacotes:
    if pacote.haslayer("IP"):
        endereco_origem = pacote[IP].src
        endereco_destino = pacote[IP].dst
        contador_origem[endereco_origem] += 1
        contador_destino[endereco_destino] += 1

top_10_origem = sorted(contador_origem.items(), key=lambda x: x[1], reverse=True)[:10]
top_10_destino = sorted(contador_destino.items(), key=lambda x: x[1], reverse=True)[:10]




# ARP

arquivo_arp = "./Data/arp.pcap"

pacotes = rdpcap(arquivo_arp)

    # Filtra os pacotes ARP
pacotes_arp = [pac for pac in pacotes if ARP in pac]

    # Cria um dicionário para contar as combinações de endereço IP e MAC
communication_count = defaultdict(int)
for pacote in pacotes_arp:
    if pacote[ARP].op == 1:  # ARP request
        src_ip = pacote[ARP].psrc
        src_mac = pacote[ARP].hwsrc
        communication_count[(src_ip, src_mac)] += 1

    # Obtém as 10 combinações mais frequentes
top_5_arp = sorted(communication_count.items(), key=lambda x: x[1], reverse=True)[:5]



matriz_top_5_arp = []
for (ip, mac), freq in top_5_arp:
    matriz_top_5_arp.append([ip, mac, freq])

#print("\nMatriz de Dados (ordenada por frequência decrescente):")
#for row in matriz_top_5_arp:
    #print(row)


# RIP

def extrair_tabelas_roteamento(pcap_file):
    tabelas_roteadores = []  # Estrutura para armazenar as tabelas

    # Carregar o arquivo pcap
    pkts = rdpcap(pcap_file)

    # Iterar pelos pacotes
    for pkt in pkts:
        if pkt.haslayer(RIP):
            rotas = []

            # Acessar as entradas de rota no pacote RIP
            for entry in pkt[RIP].payload:  # Acessa o payload das entradas
                # Verificar se a entrada é válida
                if entry.AF == 2:  # Apenas se for do tipo IP
                    rota = [
                        'Roteador 1' if pkt[IP].src == '10.0.0.1' else 'Roteador 2',
                        entry.addr,
                        entry.metric,
                        entry.mask,
                        entry.nextHop,
                    ]
                    rotas.append(rota)

            # Adiciona as rotas ao vetor de tabelas
            tabelas_roteadores.extend(rotas)

    return tabelas_roteadores

# Exemplo de uso
arquivo_pcap = "./Data/rip.pcap"
tabelas_rotas = extrair_tabelas_roteamento(arquivo_pcap)

# Impressão dos resultados
#print(tabelas_rotas)




# UDP

arquivo_udp = "./Data/udp.pcap"

pacotes = rdpcap(arquivo_udp)

pacotes_udp = defaultdict(int)

   
for pacote in pacotes:
    if pacote.haslayer("UDP"):
        pacote_udp = pacote["UDP"].dport
        pacotes_udp[pacote_udp] += 1

pacotes_udp_ordenados = sorted(pacotes_udp.items(), key=lambda x: x[1], reverse=True)

top_portas = pacotes_udp_ordenados[:4]

    # Calcula a soma das repetições das outras portas
repeticao_outras_portas = sum(repeticao for _, repeticao in pacotes_udp_ordenados[4:])

    # Adiciona "Outras portas" à lista
top_portas.append(("Outras Portas", repeticao_outras_portas))

#lista_pacotes_udp = list(pacotes_udp.items())
portas = []
for porta, repeticao in top_portas:
    portas.append([porta, repeticao])


nome_portas = []
nome_portas.append([1900, 'Microsoft SSDP'])
nome_portas.append([123, 'NTP'])
nome_portas.append([389, 'LDAP'])
nome_portas.append([53, 'DNS'])
nome_portas.append(['Outras Portas', 'Outras Portas'])

top_nome_portas = []
for porta1, repeticao in portas:
    for porta2, nome_porta in nome_portas:
        if(porta1 == porta2):
            top_nome_portas.append([nome_porta, repeticao])

#for row in top_nome_portas:
   # print(row)



# TCP

# Ler o arquivo PCAP
packets = rdpcap("./Data/tcp.pcap")

# Inicializar lista para contagens
packet_counts = []

# Definir intervalo de tempo (em segundos)
interval = 0.15

# Contar pacotes por intervalo de tempo
start_time = packets[0].time
end_time = packets[-1].time
current_time = start_time

while current_time <= end_time:
    count = sum(1 for pkt in packets if current_time <= pkt.time < current_time + interval)
    packet_counts.append(count)
    current_time += interval

# Criar um vetor de duas colunas: tempo e contagem
time_array = np.round(np.arange(0, len(packet_counts) * interval, interval), 2)
data_matrix = np.column_stack((time_array, np.array(packet_counts)))

# Criar um vetor para armazenar os valores formatados
formatted_tcp_data = np.array([[f"{row[0]:.2f}", int(row[1])] for row in data_matrix])

numeric_tcp_data = [[float(row[0]), int(row[1])] for row in formatted_tcp_data]

# Exibir o novo vetor
#print("Vetor numérico de Tempo e Contagem:")
#print(numeric_tcp_data)





# HTTP


# Definir todos os métodos HTTP possíveis
http_methods_possible = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH']

# Ler o arquivo PCAP
packets = rdpcap("./Data/http.pcap")

# Contador para métodos HTTP
http_methods_counter = Counter()

# Verificar cada pacote
for pkt in packets:
    if pkt.haslayer(HTTPRequest):
        # Contar métodos HTTP
        method = pkt[HTTPRequest].Method.decode()
        http_methods_counter[method] += 1

# Converter para lista no formato [['GET', x], ['POST', y], ...]
http_methods_list = [[method, http_methods_counter.get(method, 0)] for method in http_methods_possible]

# Exibir a lista de métodos HTTP
#print("Métodos HTTP:", http_methods_list)


# DNS

def extract_dns_queries(file_name):
    packets = rdpcap(file_name)
    dns_queries = defaultdict(int)

    for pkt in packets:
        if DNSQR in pkt and pkt.haslayer(IP):
            query_name = pkt[DNSQR].qname.decode('utf-8')
            dns_queries[query_name] += 1

    # Obter os top 10 domínios mais acessados
    sorted_queries = sorted(dns_queries.items(), key=lambda item: item[1], reverse=True)[:10]

    # Criar lista de duas colunas: domínio e número de consultas
    top_10_domains = [[domain, count] for domain, count in sorted_queries]

    return top_10_domains

arquivo_dns = "./Data/dns.pcap"
dns_queries = extract_dns_queries(arquivo_dns)

#print(dns_queries)




# SNMP


def contar_snmp_pdu(pcap_file):
    pacotes = rdpcap(pcap_file)

    pdu_count = {
        'SNMPgetRequest': 0,
        'SNMPnext': 0,
        'SNMPsetRequest': 0,
        'SNMPresponse': 0,
        'SNMPtrap': 0,
        'Outro': 0  # Para contar PDUs não especificadas e pacotes não SNMP
    }
    
    snmp_count = 0

    # Itera sobre os pacotes
    for pacote in pacotes:
        if SNMP in pacote:
            snmp_count += 1
            pdu = pacote[SNMP].PDU
            pdu_type = pdu.__class__.__name__

            # Debug: Print do tipo de PDU
            #print(f"Encontrado PDU: {pdu_type}")

            if pdu_type in pdu_count:
                pdu_count[pdu_type] += 1
            else:
                pdu_count['Outro'] += 1  # Contar outros tipos de PDU
        else:
            # Contar pacotes não SNMP como "Outro"
            pdu_count['Outro'] += 1
            #print(f"Pacote não SNMP: {pacote.summary()}")
            #print(f"Detalhes do pacote: {pacote.show()}")  # Mostra detalhes do pacote

    print(f"Número total de pacotes: {len(pacotes)}")
    print(f"Número total de pacotes SNMP: {snmp_count}")
    print(f"Número de pacotes não SNMP (contados como 'Outro'): {pdu_count['Outro']}")

    resultado = [[tipo, count] for tipo, count in pdu_count.items()]
    return resultado

# Exemplo de uso
pcap_file = "./Data/snmp.pcap"
snmp_dpus = contar_snmp_pdu(pcap_file)
#print(snmp_dpus)
