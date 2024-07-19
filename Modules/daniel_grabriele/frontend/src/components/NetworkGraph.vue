<template>
  <div class="graph">
    <v-network-graph
      :nodes="nodes"
      :edges="edges"
      :configs="configs"
      :event-handlers="eventHandlers"
    >
      <template #override-node="{ nodeId, scale, config, ...slotProps }">
        <circle
          v-bind="slotProps"
          :ref="nodeId"
          :r="config.radius * scale"
          :fill="nodes[nodeId].blocked ? 'black' : `hsl(${nodes[nodeId].hue}, 50%, 50%)`"
          :stroke="nodes[nodeId].strokeColor ?? 'white'"
          :stroke-width="size.default"
        />
      </template>
    </v-network-graph>

    <div v-if="packets.type === 0 && selectedNode" class="node-info">
      <p><strong>ID:</strong> {{ selectedPacket.identificacao }}</p>
      <p><strong>IP:</strong> {{ nodes[selectedNode].name }}</p>
      <p><strong>TTL:</strong> {{ selectedPacket.ttl }}</p>
      <p><strong>Protocolo:</strong> {{ selectedPacket.protocolo == 6 ? "TCP" : selectedPacket.protocolo == 2 ? "ICMP" : "UDP"}}</p>
    </div>
  </div>
</template>

<script>
import { nodes, edges, size, hues } from "./data";
import { configs } from "./configs";
import axios from "axios";

export default {
  props: {
    packets: Object
  },
  data() {
    return {
      nodes,
      edges,
      hues,
      size,
      selectedNode: null,
      selectedPacket: null,
      selectedRIP: null,
    };
  },

  computed: {
    configs,
    eventHandlers() {
      return {
        "node:pointerover": ({ node }) => {
          this.handleHoverNode(node, "hover");
        },

        "node:pointerout": ({ node }) => {
          this.handleHoverNode(node, "default", "lightgrey");
        },

        "edge:pointerover": ({ edge }) => {
          this.handleHoverEdge(edge, "hover");
        },

        "edge:pointerout": ({ edge }) => {
          this.handleHoverEdge(edge, "default", "lightgrey");
        },

        "node:click": ({ node }) => {
          this.handleClickNode(node);
        },
      };
    }
  },

  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets && newPackets.data && newPackets.data.length > 0) {
          this.generateNodes();
        }
      },
      deep: true
    },
    selectedNode(newVal) {
      if (newVal !== null) {
        this.updateSelectedPacket(newVal);
      }
    }
  },


  methods: {
    handleHoverNode(node, size, color) {
      const isSource = this.edges.some((edge) => edge.source === node);
      const type = isSource ? "source" : "target";

      this.edges.forEach((edge) => {
        if (edge[type] === node) {
          const defaultColor = `hsl(${edge.hue}, 50%, 50%)`;
          this.$refs[edge.source].style.stroke = color ?? defaultColor;
          this.$refs[edge.source].style.strokeWidth = this.size[size];

          this.$refs[edge.target].style.stroke = color ?? defaultColor;
          this.$refs[edge.target].style.strokeWidth = this.size[size];
        }
      });
    },

    handleClickNode(nodeId) {
      if(this.packets.type == 0) {
        if (this.selectedNode !== null) {
          this.resetNodeStyles(this.selectedNode);
        }

        this.selectedNode = nodeId;
        this.applyNodeStyles(nodeId);
      }
    },

    resetNodeStyles(nodeId) {
      const defaultColor = "lightgrey";
      this.$refs[nodeId].style.stroke = defaultColor;
      this.$refs[nodeId].style.strokeWidth = this.size.default;
    },
    
    applyNodeStyles(nodeId) {
      const selectedColor = "blue";
      this.$refs[nodeId].style.stroke = selectedColor;
      this.$refs[nodeId].style.strokeWidth = this.size.default + 2;
    },

    handleHoverEdge(edge, size, color) {
      const edgeData = this.edges[edge]; 

      if (edgeData) { 
        const { source, target, hue } = edgeData;
        const defaultColor = `hsl(${hue}, 50%, 50%)`;

        if (this.$refs[source]) {
          this.$refs[source].style.strokeWidth = this.size[size];
          this.$refs[source].style.stroke = color ?? defaultColor;
        }

        if (this.$refs[target]) {
          this.$refs[target].style.strokeWidth = this.size[size];
          this.$refs[target].style.stroke = color ?? defaultColor;
        }
      }
    },

    generateNodes() {
      if (this.packets.type === 0) {
        this.generateIpv4Nodes();
      } else if (this.packets.type === 1) {
        this.generateArpNodes();
      } else if( this.packets.type == 2){
        // this.generateRipNodes();
      } else if( this.packets.type == 3){
        this.generateUdpNodes();
        this.fetchBlockedIPs();
      }
    },

    generateIpv4Nodes() {
      this.generateIpsList();

      this.nodes = [];
      this.edges = [];

      this.ips.forEach((ip, index) => {
        const nodeIndex = index + 1;
        const nodeName = `node${nodeIndex}`;
        this.nodes[nodeName] = { name: ip, edgeWidth: 1, hue: 200 };
      });
      
      this.packets.data.forEach((pacote, index) => {
        const sourceNodeIndex = index + 1;
        const sourceNodeName = `node${sourceNodeIndex}`;
        const targetNodeIndex = this.packets.data.findIndex(p => p.ip_origem === pacote.ip_destino) + 1;
        const targetNodeName = `node${targetNodeIndex}`;
        const edgeName = `edge${index + 1}`;
        this.edges[edgeName] = { 
          source: sourceNodeName, 
          target: targetNodeName, 
          edgeWidth: 1, 
          hue: hues[Math.floor(Math.random() * hues.length)],
          dashed: sourceNodeIndex !== targetNodeIndex, 
        };
      });
    },

    generateArpNodes() {
      this.generateUniqueMacsList();

      this.nodes = [];
      this.edges = [];

      this.ips.forEach((ip, index) => {
        const nodeIndex = index + 1;
        const nodeName = `node${nodeIndex}`;
        this.nodes[nodeName] = { name: ip, edgeWidth: 1, hue: 200 };
      });

      // Criação das edges com base nos pacotes ARP
      this.packets.data.forEach((pacote, index) => {
        const sourceNodeIndex = this.ips.indexOf(pacote.sender_hardware_address) + 1;
        const sourceNodeName = `node${sourceNodeIndex}`;
        const targetNodeIndex = this.ips.indexOf(pacote.target_hardware_address) + 1;
        const targetNodeName = `node${targetNodeIndex}`;
        const edgeName = `edge${index + 1}`;
        
       
        this.edges[edgeName] = {
          source: sourceNodeName,
          target: targetNodeName,
          edgeWidth: 1,
          hue: hues[Math.floor(Math.random() * hues.length)],
        };
        
      });
    },

    generateRipNodes() {
      this.nodes = [];
      this.edges = [];

      // Mapa para rastrear nós únicos por IP
      const ipToNodeMap = new Map();

      // Processar cada pacote RIP para criar nós e arestas
      if (Array.isArray(this.packets.data)) {
        this.packets.data.forEach((packet, index) => {
          const sourceIp = packet.source_ip;
          const destinationIp = packet.destination_ip;

          // Verificar e adicionar nós se não existirem
          if (!ipToNodeMap.has(sourceIp)) {
            ipToNodeMap.set(sourceIp, { id: `node${this.nodes.length + 1}`, name: sourceIp });
            this.nodes.push(ipToNodeMap.get(sourceIp));
          }
          if (!ipToNodeMap.has(destinationIp)) {
            ipToNodeMap.set(destinationIp, { id: `node${this.nodes.length + 1}`, name: destinationIp });
            this.nodes.push(ipToNodeMap.get(destinationIp));
          }

          // Criar aresta entre os nós
          const sourceNode = ipToNodeMap.get(sourceIp);
          const targetNode = ipToNodeMap.get(destinationIp);
          this.edges.push({
            id: `edge${index + 1}`,
            source: sourceNode.id,
            target: targetNode.id,
          });
        });
      }
    },

    generateUdpNodes() {
      if (!this.packets || !this.packets.data || this.packets.data.length === 0) {
        return;
      }

      this.generateIpsList();

      this.nodes = [];
      this.edges = [];

      this.ips.forEach((ip, index) => {
        const nodeIndex = index + 1;
        const nodeName = `node${nodeIndex}`;
        this.nodes[nodeName] = { name: ip, edgeWidth: 1, hue: 200, blocked: false }; 
      });

      this.packets.data.forEach((packet, index) => {
        const sourceNodeIndex = this.ips.indexOf(packet.ip_origem) + 1;
        const sourceNodeName = `node${sourceNodeIndex}`;
        const targetNodeIndex = this.ips.indexOf(packet.ip_destino) + 1;
        const targetNodeName = `node${targetNodeIndex}`;
        const edgeName = `edge${index + 1}`;

        if (packet.anomalias && packet.anomalias.length > 0) {
          this.nodes[sourceNodeName].hue = 0; // Define a cor para vermelho
          this.nodes[targetNodeName].hue = 0; // Define a cor para vermelho
        }

        this.edges[edgeName] = {
          source: sourceNodeName,
          target: targetNodeName,
          edgeWidth: 1,
          hue: hues[Math.floor(Math.random() * hues.length)],
        };        
      });
    },

    convertPacketsToObject() {
      if (!this.packets || !this.packets.data || this.packets.data.length === 0) {
        return;
      }

      const packetsObject = this.packets.data.reduce((obj, packet) => {
        const key = `${packet.ip_origem}-${packet.ip_destino}`;
        obj[key] = packet;
        return obj;
      }, {});

      this.packetsObject = packetsObject;
    },

    async fetchBlockedIPs() {
      try {
        const response = await axios.get("http://localhost:8000/ips_bloqueados");
        this.blockedIPs = response.data.ips_bloqueados;

        // Após 3 segundos, bloqueia os IPs
        setTimeout(() => {
          this.blockIPs();
        }, 3000);

        // Após 8 segundos, desbloqueia os IPs
        setTimeout(() => {
          this.unblockIPs();
        }, 8000);
      } catch (error) {
        console.error("Erro ao buscar IPs bloqueados:", error);
      }
    },
    
    blockIPs() {
      this.blockedIPs.forEach(ip => {
        const node = Object.values(this.nodes).find(node => node.name === ip);
        if (node) {
          node.blocked = true; 
          this.updateNodeStyle(node.id);
        }
      });
    },

    unblockIPs() {
      this.blockedIPs.forEach(ip => {
        const node = Object.values(this.nodes).find(node => node.name === ip);
        if (node) {
          node.blocked = false; 
          this.updateNodeStyle(node.id);
        }
      });
    },

    updateNodeStyle(nodeId) {
      const defaultColor = "blue";

      if (this.$refs[nodeId]) {
        this.$refs[nodeId].style.stroke = defaultColor;
        this.$refs[nodeId].style.strokeWidth = this.size.default + 2;
      }
    },

    async checkBlockedIPsExpiry() {
      const currentTimestamp = new Date().getTime();

      // Itera sobre os IPs bloqueados para verificar se algum já pode ser desbloqueado
      Object.keys(this.blockedIPs).forEach(ip => {
        if (this.blockedIPs[ip] <= currentTimestamp) {
          // Remove o IP da lista de bloqueados
          delete this.blockedIPs[ip];

          const node = Object.values(this.nodes).find(node => node.name === ip);
          if (node) {
            node.blocked = false;
          }

          console.log(`IP desbloqueado automaticamente: ${ip}`);
        }
      });
    },

    generateIpsList() {
      const ipsOrigem = this.packets.data.map(pacote => pacote.ip_origem);
      const ipsDestino = this.packets.data.map(pacote => pacote.ip_destino);

      // Combina os dois arrays
      const todosIps = [...ipsOrigem, ...ipsDestino];

      // Remove os valores duplicados
      this.ips = todosIps.filter((ip, index) => todosIps.indexOf(ip) === index);
    },

    generateUniqueMacsList() {
      const ipsOrigem = this.packets.data.map(packet => packet.sender_hardware_address);
      const ipsDestino = this.packets.data.map(packet => packet.target_hardware_address);

      // Combina os dois arrays
      const todosIps = [...ipsOrigem, ...ipsDestino];

      // Remove os valores duplicados
      this.ips = todosIps.filter((ip, index) => todosIps.indexOf(ip) === index);
    },

    updateSelectedPacket(nodeId) {
      const selectedIP = this.nodes[nodeId].name;
      this.selectedPacket = this.packets.data.find(packet => 
        packet.ip_origem === selectedIP || packet.ip_destino === selectedIP
      );
    },
  }
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}

.graph {
  width: 100vw;
  height: 100vh;
  position: relative;
}

.node-info {
  position: fixed;
  top: 10px;
  right: 20px;
  background: white;
  padding: 5px 10px;
  border: 1px solid lightgrey;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: justify;
}
</style>
