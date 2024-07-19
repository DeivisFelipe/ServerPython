<template>
  <div class="packet-traffic">
    <h2 class="chart-title">Visualização de Tráfego de Pacotes ARP</h2>
    <div class="chart-container">
      <canvas ref="packetChart"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js';

export default {
  name: 'PacketTraffic',
  props: {
    packetData: {
      type: Array,
      required: true
    }
  },
  mounted() {
    this.renderPacketChart();
  },
  methods: {
    renderPacketChart() {
      const ctx = this.$refs.packetChart.getContext('2d');

      // Usar Set para garantir endereços MAC únicos
      const macAddresses = new Set();
      this.packetData.forEach(packet => {
        macAddresses.add(packet.sender_hardware_address);
        macAddresses.add(packet.target_hardware_address);
      });

      // Converter Set para array
      const labels = Array.from(macAddresses);
      
      // Inicializar contadores para solicitações e respostas
      const requests = new Array(labels.length).fill(0);
      const replies = new Array(labels.length).fill(0);

      // Agrupar dados por endereço MAC e contar solicitações e respostas
      this.packetData.forEach(packet => {
        const senderIndex = labels.indexOf(packet.sender_hardware_address);
        const targetIndex = labels.indexOf(packet.target_hardware_address);
        
        if (packet.operation === 1) {  // Solicitação ARP
          if (senderIndex !== -1) requests[senderIndex] += 1;
          if (targetIndex !== -1) requests[targetIndex] += 1;
        } else if (packet.operation === 2) {  // Resposta ARP
          if (senderIndex !== -1) replies[senderIndex] += 1;
          if (targetIndex !== -1) replies[targetIndex] += 1;
        }
      });

      // Configurações do gráfico
      const config = {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Solicitações ARP',
              data: requests,
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgb(75, 192, 192)',
              borderWidth: 1
            },
            {
              label: 'Respostas ARP',
              data: replies,
              backgroundColor: 'rgba(192, 75, 75, 0.2)',
              borderColor: 'rgb(192, 75, 75)',
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: 'Endereço MAC'
              }
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Contagem'
              }
            }
          }
        }
      };

      // Renderizar o gráfico usando Chart.js
      this.packetChart = new Chart(ctx, config);
    }
  },
  watch: {
    packetData: {
      handler() {
        // Atualizar o gráfico quando os dados mudarem
        this.packetChart.destroy();
        this.renderPacketChart(); 
      },
      deep: true
    }
  },
  beforeUnmount() {
    if (this.packetChart) {
      this.packetChart.destroy();
    }
  }
};
</script>

<style scoped>
.packet-traffic {
  max-width: 100%;
  margin: auto;
  padding: 20px;
  text-align: center;
}

.chart-container {
  display: flex;
  justify-content: center; 
  align-items: center; 
  height: 400px;
  overflow: hidden;
}

.chart-title {
  text-align: center;
  margin-bottom: 10px;
  font-size: 18px;
  color: #333;
}

.packet-traffic {
  border: none;
  border-radius: 0;
}
</style>
