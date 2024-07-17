from flask import Flask, jsonify, render_template
from modules import trabalho_1
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
from flask import Flask, jsonify
from scapy.all import rdpcap, UDP, RIP
from datetime import datetime

from scapy.all import rdpcap, UDP, RIP
from flask import Flask, jsonify
from datetime import datetime

@app.route('/api/origem/data')
@cross_origin()
def get_top_origem():
    return jsonify(trabalho_1.top_10_origem)


@app.route('/api/destino/data')
@cross_origin()
def get_top_destino():
    return jsonify(trabalho_1.top_10_destino)

@app.route('/api/arp/data')
@cross_origin()
def get_top_arp():
    return jsonify(trabalho_1.matriz_top_5_arp)

@app.route('/api/rip/data')
@cross_origin()
def get_top_rip():
    return jsonify(trabalho_1.tabelas_rotas)

@app.route('/api/udp/data')
@cross_origin()
def get_top_udp():
    return jsonify(trabalho_1.top_nome_portas)

@app.route('/api/tcp/data')
@cross_origin()
def get_latencia_tcp():
    return jsonify(trabalho_1.numeric_tcp_data)

@app.route('/api/http/data')
@cross_origin()
def get_top_http():
    return jsonify(trabalho_1.http_methods_list)

@app.route('/api/dns/data')
@cross_origin()
def get_dns():
    return jsonify(trabalho_1.dns_queries)

@app.route('/api/snmp/data')
@cross_origin()
def get_snmp():
    return jsonify(trabalho_1.snmp_dpus)


if __name__ == '__main__':
    app.run()
