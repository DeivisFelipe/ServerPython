<template>
  <div class="chart-container">
    <h2 class="chart-title">Contagem de Protocolos UDP</h2>
    <canvas id="udpChart"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: {
    udpNodes: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      chart: null,
      protocolCountData: {},
      protocolAnomalies: {}, 
      protocolIPs: {},         
     selectedProtocol: null 
    };
  },
  mounted() {
    this.countProtocolTypes();  
    window.addEventListener('resize', this.renderChart);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.renderChart);
    this.destroyChart();
  },
  methods: {
    countProtocolTypes() {
      // Contar ocorrências de cada tipo de protocolo UDP
      const contador = this.countProtocolOccurrences();

      // Atualizar os dados de contagem de protocolos
      this.protocolCountData = contador;

      // Inicializar estruturas para anomalias e IPs
      this.protocolAnomalies = {};
      this.protocolIPs = {};

      // Calcular anomalias e IPs por protocolo
      this.calculateProtocolDetails();

      // Renderizar o gráfico com os dados atualizados
      this.renderChart();
    },
    countProtocolOccurrences() {
      // Inicializar contador
      const contador = {};

      // Contar ocorrências de cada tipo de protocolo UDP
      this.udpNodes.forEach(node => {
        const protocolo = node.protocolo;
        if (contador[protocolo]) {
          contador[protocolo].count += 1;
        } else {
          contador[protocolo] = { count: 1 };
        }
      });

      return contador;
    },
    calculateProtocolDetails() {
      // Inicializar estruturas para armazenar anomalias e IPs
      for (const protocolo in this.protocolCountData) {
        this.protocolAnomalies[protocolo] = [];
        this.protocolIPs[protocolo] = [];
      }

      // Preencher anomalias e IPs por protocolo
      this.udpNodes.forEach(node => {
        const protocolo = node.protocolo;
        if (node.anomalias.length > 0) {
          node.anomalias.forEach(anomaly => {
            if (!this.protocolAnomalies[protocolo].includes(anomaly)) {
              this.protocolAnomalies[protocolo].push(anomaly);
            }
          });
        }
        if (!this.protocolIPs[protocolo].includes(node.ip_origem)) {
          this.protocolIPs[protocolo].push(node.ip_origem);
        }
      });
    },
    renderChart() {
      const ctx = document.getElementById('udpChart').getContext('2d');
      this.destroyChart();

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Object.keys(this.protocolCountData),
          datasets: [{
            label: 'Quantidade',
            data: Object.values(this.protocolCountData).map(item => item.count),
            backgroundColor: [
              'rgba(255, 99, 132, 0.6)',
              'rgba(54, 162, 235, 0.6)',
              'rgba(255, 206, 86, 0.6)',
              'rgba(75, 192, 192, 0.6)',
              'rgba(153, 102, 255, 0.6)',
              'rgba(255, 159, 64, 0.6)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Quantidade'
              }
            }
          }
        }
      });
    },
    destroyChart() {
      if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
    },
  }
};
</script>

<style scoped>
.chart-container {
  margin-top: 20px;
  height: 90%;
}

</style>
