from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import pyshark
import matplotlib.pyplot as plt
import plotly.io as pio
import base64
from .analises_e_valores import *
import asyncio
from concurrent.futures import ThreadPoolExecutor

def index(request):
    return HttpResponse("Olá, mundo. Esta é a página inicial do meu aplicativo.")


def cria_grafico_dinamico(categorias, valores, titulo='Gráfico de Barras', cor='blue', largura=6, altura=6):
    # Verificar se o número de categorias corresponde ao número de valores
    if len(categorias) != len(valores):
        raise ValueError("O número de categorias deve ser igual ao número de valores.")
    
    # Criando o gráfico de barras dinâmico
    plt.figure(figsize=(largura, altura))
    plt.bar(categorias, valores, color=cor)
    plt.xlabel('Nomes')
    plt.ylabel('Valores')
    plt.title(titulo)

    # Salvando o gráfico como imagem em base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Fechando a figura para liberar memória
    plt.close()

    return image_base64

def charts_view(request):
    categorias = ['bobalhão', 'boboca', 'bobinho']
    valores = [10, 20, 15]
    titulo = 'Exemplo de Gráfico de Barras'
    cor = 'green'
    image_base64 = cria_grafico_dinamico(categorias, valores, titulo, cor, largura=8, altura=4)

    ip_comum, ip_destino_comum = analise_ipv4()
    
    # Criar listas para categorias e valores
    categorias_ips = []
    valores_ips = []

    # Adicionar categorias e valores para ip_comum
    for ip, count in ip_comum:
        categorias_ips.append(f'IP src: {ip}')
        valores_ips.append(count)

    # Adicionar categorias e valores para ip_destino_comum
    for ip, count in ip_destino_comum:
        categorias_ips.append(f'IP dst: {ip}')
        valores_ips.append(count)

    titulo_ips = 'ips mais comuns do ipv4'
    cor_ips = 'purple'
    image_trabalho_1_ips = cria_grafico_dinamico(categorias_ips, valores_ips, titulo_ips, cor_ips, largura=18, altura=6)

    # Incluir os gráficos no contexto
    context = {
        'grafico_base64': image_base64,
        'trabalho_1_ips': image_trabalho_1_ips
    }

    return render(request, 'charts.html', context)

"""
def charts(request):

    #########################################################################################################

    x_data = [1, 2, 3, 4, 5]
    y_data = [2, 3, 4, 5, 6]
    trace = go.Scatter(x=x_data, y=y_data, mode='markers')
    layout = go.Layout(title='Teste Inicial', xaxis=dict(title='Eixo X'), yaxis=dict(title='Eixo Y'))
    fig = go.Figure(data=[trace], layout=layout)
    primeiro_grafico = go.Figure.to_html(fig, include_plotlyjs=False)

    #########################################################################################################

    ips = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
    frequencia = [100, 150, 200, 250]
    sorted_ips = [ip for _, ip in sorted(zip(frequencia, ips), reverse=True)]
    sorted_frequencia = sorted(frequencia, reverse=True)
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=[sorted_frequencia],
        x=sorted_ips,
        y=['Frequencia'],
        colorscale='Viridis'))
    segundo_grafico = go.Figure.to_html(fig_heatmap, include_plotlyjs=False)

    # Renderiza ambos os gráficos na página
    context = {'primeiro_grafico': primeiro_grafico, 'segundo_grafico': segundo_grafico}
    leitor_ip()
    return render(request, 'charts.html', context)
"""


def leitor_ip():
    pcap_file = 'Pacote_de_rede.pcap'
    cap = pyshark.FileCapture(pcap_file) # Leio o pacote

    for packet in cap: # Itero sobre pacote
        if 'IP' in packet: # Verifico se existe a chave IP dentro do dicionário packet (in funciona diferente em cada tipo de dado)
            ip_src = packet.ip.src
            ip_dst = packet.ip.dst
            #print(dir(packet))
            #packet.pretty_print()
            #packet.interface_captured()
    


"""
def charts(request):
    # Dados de exemplo
    data = {
        'labels': ['A', 'B', 'C', 'D'],
        'datasets': [{
            'label': 'Exemplo',
            'data': [12, 19, 3, 5],
        }]
    }

    chart = BarChart(data)
    return JsonResponse(chart.to_dict())
"""
