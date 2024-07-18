import pyshark
from collections import Counter
import pickle
import os

def capturar_pacotes(file_path):
    capture = pyshark.FileCapture(file_path)
    pacotes = list(capture)  # Lê todos os pacotes do arquivo e armazena em uma lista
    capture.close()  # Fecha o FileCapture após ler todos os pacotes
    return pacotes

def salvar_pacotes_em_arquivo(pacotes, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(pacotes, f)

def carregar_pacotes_do_arquivo(file_path):
    with open(file_path, 'rb') as f:
        pacotes = pickle.load(f)
    return pacotes

def analise_ipv4_script(pacotes):
    src_ips = Counter()
    dst_ips = Counter()

    for packet in pacotes:
        if 'IP' in packet:
            src_ips[packet.ip.src] += 1
            dst_ips[packet.ip.dst] += 1

    # Obtém os 10 IPs de origem mais comuns
    most_common_src_ips = src_ips.most_common(10)

    # Obtém os 10 IPs de destino mais comuns
    most_common_dst_ips = dst_ips.most_common(10)

    return most_common_src_ips, most_common_dst_ips


def analise_ipv4():
    # Obtém o diretório atual do script
    script_dir = os.path.dirname(__file__)

    # Monta o caminho completo para o arquivo de pacotes
    file_path = os.path.join(script_dir, 'pacotes_ipv4_lidos.pcap')

    # Carrega os pacotes do arquivo
    pacotes_carregados = carregar_pacotes_do_arquivo(file_path)

    # Realiza a análise dos pacotes
    resultado_analise = analise_ipv4_script(pacotes_carregados)
    return resultado_analise

# Exibe resultados
#for ip, count in resultado_analise:
#    print(f"IP: {ip}, Contagem: {count}")
