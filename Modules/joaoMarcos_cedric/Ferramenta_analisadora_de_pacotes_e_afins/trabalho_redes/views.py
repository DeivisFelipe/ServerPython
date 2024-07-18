from django.shortcuts import render
from django.http import HttpResponse
import pyshark
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def index(request):
    return HttpResponse("Olá, mundo. Esta é a página inicial do meu aplicativo.")

def charts_view(request):
    # Dados do gráfico (exemplo)
    categorias = ['bobão 1', 'bobalhão 2', 'bobinho 3']
    valores = [10, 20, 15]

    # Criando o gráfico inicial que servirá de base para o resto
    plt.figure(figsize=(6, 6))
    plt.bar(categorias, valores, color='blue')
    plt.xlabel('Tipos de bobo')
    plt.ylabel('Valores')
    plt.title('Gráfico de Barras Simples')

    # Salvar o gráfico em um buffer de bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Incluir o gráfico na context
    context = {
        'grafico_base64': image_base64
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
