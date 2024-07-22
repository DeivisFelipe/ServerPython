<template>
  <div class="snmp-chart-container">
    <!-- Gráfico de contagem de requisições e respostas SNMP -->
    <div class="chart-wrapper">
      <canvas ref="snmpCountChart" class="chart"></canvas>
    </div>

    <!-- Gráfico de latência SNMP -->
    <div class="chart-wrapper">
      <canvas ref="snmpLatencyChart" class="chart"></canvas>
    </div>

    <!-- Gráfico de pizza para tipos de comandos SNMP -->
    <div class="chart-wrapper">
      <canvas ref="snmpCommandPieChart" class="chart"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: {
    packets: Object
  },
  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets && newPackets.data.length > 0) {
          this.generateSnmpCountChartData(newPackets.data);
          this.generateSnmpLatencyChartData(newPackets.data);
          this.generateSnmpCommandPieChartData(newPackets.data);
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    generateSnmpCountChartData(packets) {
      let requestCount = 0;
      let responseCount = 0;

      packets.forEach(packet => {
        if (packet.comando.includes('SNMPnext')) {
          requestCount++;
        } else if (packet.comando.includes('SNMPresponse')) {
          responseCount++;
        }
      });

      this.renderSnmpCountChart(requestCount, responseCount, this.$refs.snmpCountChart.getContext('2d'));
    },
    renderSnmpCountChart(requestCount, responseCount, ctx) {
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Requests', 'Responses'],
          datasets: [{
            label: 'SNMP Requests and Responses',
            data: [requestCount, responseCount],
            backgroundColor: ['rgba(54, 162, 235, 0.2)', 'rgba(153, 102, 255, 0.2)'],
            borderColor: ['rgba(54, 162, 235, 1)', 'rgba(153, 102, 255, 1)'],
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
                text: 'Count'
              }
            }
          }
        }
      });
    },
    generateSnmpLatencyChartData(packets) {
      let timestamps = packets.map(packet => packet.timestamp);
      let latencies = [];

      for (let i = 1; i < timestamps.length; i++) {
        let latency = timestamps[i] - timestamps[i - 1];
        latencies.push(latency.toFixed(2)); // Arredonda a latência para 2 casas decimais
      }

      // Verifique os dados de latência gerados
      console.log('Latencies:', latencies);

      this.renderSnmpLatencyChart(latencies, this.$refs.snmpLatencyChart.getContext('2d'));
    },
    renderSnmpLatencyChart(latencies, ctx) {
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: latencies.map((_, index) => `Packet ${index + 1}`),
          datasets: [{
            label: 'SNMP Packet Latency (ms)',
            data: latencies,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
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
                text: 'Latency (ms)'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Packet Index'
              }
            }
          }
        }
      });
    },
    generateSnmpCommandPieChartData(packets) {
      let commandCounts = {};

      packets.forEach(packet => {
        if (commandCounts[packet.comando]) {
          commandCounts[packet.comando]++;
        } else {
          commandCounts[packet.comando] = 1;
        }
      });

      let labels = Object.keys(commandCounts);
      let data = Object.values(commandCounts);

      this.renderSnmpCommandPieChart(labels, data, this.$refs.snmpCommandPieChart.getContext('2d'));
    },
    renderSnmpCommandPieChart(labels, data, ctx) {
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: 'SNMP Command Distribution',
            data: data,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)'
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
          maintainAspectRatio: false
        }
      });
    }
  }
};
</script>

<style scoped>
.snmp-chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.chart-wrapper {
  width: 90%;
  max-width: 800px; /* Ajuste conforme necessário */
  margin-bottom: 20px;
}

.chart {
  width: 100%;
  height: 400px; /* Define uma altura fixa para os gráficos */
}
</style>
