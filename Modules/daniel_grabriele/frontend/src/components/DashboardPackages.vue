<template>
  <div class="page">
    <!-- Botão para mostrar gráficos -->
    <label for="showGraphBtn" class="float-button-top btn-floating-top" v-if="showGraphButton">
      <div class="icon-container" @click="mostrarModalGraficos('graph')">
        <n-icon size="24">
          <bar-chart/>
        </n-icon>
      </div>
    </label>

    <!-- Botão para mostrar informações -->
    <label for="showInfoBtn" class="float-button-top btn-floating-top info-button" 
           :style="{'top': showGraphButton ? '80px' : '20px'}"
           v-if="showInfoButton">
      <div class="icon-container" @click="mostrarModalGraficos('info')">
        <n-icon size="24">
          <information-circle/>
        </n-icon>
      </div>
    </label>

    <!-- Modal de gráficos/informações -->
    <div v-if="showModalGraphics" class="modal-background">
      <div class="modal-content">
        <span class="close" @click="fecharModalGraficosIPv4">&times;</span>

        <graphics-page v-if="showGraphicsIPv4" :packets="packets" />
        <packet-traffic v-if="showGraphicsARP" :packetData="packets.data" />
        <rip-nodes-table v-if="showInfoRIP" :ripNodes="packets.data" />
        <udp-nodes-table v-if="showInfoUDP" :udpNodes="packets.data" />
        <udp-graphics v-if="showGraphicsUDP" :udpNodes="packets.data" />
        <dns-nodes-table v-if="showInfoDNS" :dnsPackages="packets.data" />
        <http-table v-if="showInfoHttp" :requests="packets.data" />
        <snmp-nodes-table v-if="showInfoSnmp" :snmpNodes="packets.data" />
      </div>
    </div>

    <!-- Botão de upload de arquivo -->
    <label for="fileInput" class="float-button btn-floating">
      <div class="icon-container">
        <n-icon size="24">
          <cloud-upload/>
        </n-icon>
      </div>
    </label>
    <input id="fileInput" ref="fileInput" type="file" style="display: none" @change="uploadArquivo">
    
    <div v-if="packets.type == 4">
      <analise-tcp class="graph" :packets="packets" />
    </div>
    <div v-if="packets.type == 2">
      <rip-graphics class="graph" :packets="packets" />
    </div>
    <div v-if="packets.type == 5">
      <dns-graphics class="graph" :packets="packets" />
    </div>
    <div v-if="packets.type == 6">
      <http-graphics class="graph" :packets="packets" />
    </div>
    <div v-if="packets.type == 7">
      <snmp-graphics class="graph" :packets="packets" />
    </div>
    <div v-else class="graph-container">
      <network-graph class="graph" :packets="packets" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import NetworkGraph from "./NetworkGraph.vue";
import { NIcon } from "naive-ui";
import { CloudUpload, BarChart, InformationCircle } from "@vicons/ionicons5";
import GraphicsPage from './GraphicsPage.vue';
import PacketTraffic from './PacketTraffic.vue';
import RipNodesTable from './RipNodesTable.vue'; 
import UdpNodesTable from './UdpNodesTable.vue'; 
import UdpGraphics from './UdpGraphics.vue';
import AnaliseTcp from './AnaliseTcp.vue';
import DnsNodesTable from './DnsNodesTable.vue';
import RipGraphics from './RipGraphics.vue';
import DnsGraphics from './DnsGraphics.vue'
import HttpGraphics from './HttpGraphics.vue';
import HttpTable from './HttpsTable.vue';
import SnmpGraphics from './SnmpGraphics.vue';
import SnmpNodesTable from './SnmpNodesTable.vue';

export default {
  name: 'DashboardPackages',
  components: {
    NetworkGraph,
    NIcon,
    CloudUpload,
    BarChart,
    InformationCircle,
    GraphicsPage,
    PacketTraffic,
    RipNodesTable,
    UdpNodesTable,
    UdpGraphics,
    AnaliseTcp,
    DnsNodesTable,
    RipGraphics,
    DnsGraphics,
    HttpGraphics,
    HttpTable,
    SnmpGraphics,
    SnmpNodesTable
  },
  data() {
    return {
      packets: {
        type: -1,
        data: [],
        network: []
      },
      showGraphButton: false,
      showInfoButton: false,
      showModalGraphics: false,
      showGraphicsIPv4: false,
      showGraphicsARP: false,
      showGraphicsUDP: false,
      showInfoRIP: false,
      showInfoUDP: false,
      showInfoDNS: false,
      showInfoHttp: false,
      showInfoSnmp: false
    };
  },
  methods: {
    async uploadArquivo(event) {
      const arquivo = event.target.files[0];
      
      if (!arquivo) {
        console.error("Nenhum arquivo selecionado.");
        return;
      }

      const formData = new FormData();
      formData.append("pcap_file", arquivo);

      try {
        const fileExtension = this.getFileExtension(arquivo.name);

        if (fileExtension === "pcapng") {
          this.packets.type = 0; // IPv4
          const response = await this.getIpv4Packets(formData);
          this.packets.data = response.data.pacotes;
          this.showGraphButton = true; // Mostra o botão de gráfico
          this.showInfoButton = false;
        } else if (fileExtension === "pcap") {
          const protocolName = this.getProtocolName(arquivo.name);
         
          if (protocolName === "ipv4") {
            this.packets.type = 0; // IPv4
            const response = await this.getIpv4Packets(formData);
            this.packets.data = response.data.pacotes;
            this.showGraphButton = true; // Mostra o botão de gráfico
            this.showInfoButton = false;
          } else if (protocolName === "arp") {
            this.packets.type = 1; // ARP
            const response = await this.getArpPackets(formData);
            this.packets.data = response.data.pacotes;
            this.showGraphButton = true; // Mostra o botão de gráfico
            this.showInfoButton = false;
          } else if (protocolName === "rip") {
            this.packets.type = 2; // RIP 
            const response = await this.getRipPackets(formData);
            this.packets.data = response.data.pacotes;
            this.showGraphButton = false; 
            this.showInfoButton = false;
          } else if (protocolName === "udp") {
            this.packets.type = 3; // UDP
            const response = await this.getUdpPackets(formData);
            this.packets.data = response.data.pacotes;
            this.showGraphButton = true;
            this.showInfoButton = true;
          } else if (protocolName === "tcp") {
            this.packets.type = 4; // TCP
            const response = await this.getTcpPackets(formData);
            this.packets.data = response.data.pacotes;
            this.packets.network = response.data.conexoes;
            this.showGraphButton = false;
            this.showInfoButton = false;
          } else if (protocolName === "dns") {
            this.packets.type = 5; // DNS
            const response = await this.getDnsPackets(formData);
            this.packets.data = response.data.pacotes;
            this.showGraphButton = false;
            this.showInfoButton = true;
          } else if (protocolName === "http") {
            this.packets.type = 6; // HTTP
            const response = await this.getHttpPackets(formData);
            this.packets.data = response.data.pacotes;
            this.showGraphButton = false;
            this.showInfoButton = true;
          } else if (protocolName === "snmp") {
            this.packets.type = 7; // SNMP
            const response = await this.getSnmpPackets(formData);
            this.packets.data = response.data.pacotes;
            console.log(this.packets)
            this.showGraphButton = false;
            this.showInfoButton = true;
          } else {
            throw new Error("Protocolo não suportado: " + protocolName);
          }
        } else {
          throw new Error("Formato de arquivo não suportado.");
        }
      } catch (error) {
        console.error("Erro ao enviar arquivo:", error);
      }
    },

    mostrarModalGraficos(type) {
      this.showModalGraphics = true;
      if (type === 'graph') {
        if (this.packets.type === 0) {
          this.showGraphicsIPv4 = true;
        } else if (this.packets.type === 1) {
          this.showGraphicsARP = true;
        } else if (this.packets.type === 3) {
          this.showGraphicsUDP = true;
        }
      } else if (type === 'info') {
        if (this.packets.type === 2) {
          this.showInfoRIP = true;
        } else if (this.packets.type === 3) {
          this.showInfoUDP = true;
        } else if(this.packets.type === 5) {
          this.showInfoDNS = true;
        } else if(this.packets.type == 6){
          this.showInfoHttp = true;
        } else if(this.packets.type == 7) {
          this.showInfoSnmp = true;
        }
      }
    },

    fecharModalGraficosIPv4() {
      this.showModalGraphics = false;
      this.showGraphicsIPv4 = false;
      this.showGraphicsARP = false;
      this.showGraphicsUDP = false;
      this.showInfoRIP = false;
      this.showInfoUDP = false;
      this.showInfoSnmp = false;
    },

    getFileExtension(fileName) {
      return fileName.split(".").pop().toLowerCase();
    },

    getProtocolName(fileName) {
      const baseName = fileName.split(".")[0].toLowerCase();
      if (baseName.includes("ipv4")) {
        return "ipv4";
      } else if (baseName.includes("arp")) {
        return "arp";
      } else if (baseName.includes("rip")) {
        return "rip";
      } else if (baseName.includes("udp")) {
        return "udp";
      } else if (baseName.includes("tcp")) {
        return "tcp";
      } else if (baseName.includes("dns")) {
        return "dns";
      } else if (baseName.includes("http")) {
        return "http"
      } else if (baseName.includes("snmp")) {
        return "snmp"
      } else {
        throw new Error("Protocolo não identificado pelo nome do arquivo.");
      }
    },

    async getIpv4Packets(formData) {
      return await axios.post("http://localhost:8000/ipv4/list_packages", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    },

    async getArpPackets(formData) {
      return await axios.post("http://localhost:8000/arp/list_packages", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    },

    async getRipPackets(formData) {
      return await axios.post("http://localhost:8000/rip/listar_pacotes", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    },

    async getUdpPackets(formData) {
      return await axios.post("http://localhost:8000/udp/list_packages", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    },

    async getTcpPackets(formData) {
      return await axios.post("http://localhost:8000/tcp/list_packages", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    },

    async getDnsPackets(formData) {
      return await axios.post("http://localhost:8000/dns/listar_pacotes", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    },

    async getHttpPackets(formData) {
      return await axios.post("http://localhost:8000/http/listar_pacotes", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    },

    async getSnmpPackets(formData) {
      return await axios.post("http://localhost:8000/snmp/listar_pacotes", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    },
  },
};
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  min-height: 100vh; 
}

.float-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}

.float-button-top {
  position: fixed;
  top: 20px; 
  left: 20px;
  z-index: 9999;
}

.info-button {
  top: 80px;
}

.btn-floating, .btn-floating-top {
  background-color: #232343;
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0px 0px 5px rgba(112, 106, 106, 0.5);
}

.icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.graph-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.graph {
  width: 100%;
  height: 100%;
  background-color: rgb(222, 235, 235);
}

.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  width: 80%;
  height: 80%;
  overflow: auto;
}

.modal-close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  background-color: #ddd;
  border: none;
  cursor: pointer;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

</style>
