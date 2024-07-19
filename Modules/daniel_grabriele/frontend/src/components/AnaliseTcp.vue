<template>
  <div class="central-container">
    <div class="flag-count-chart">
      <!-- Gráfico de contagem de flags e retransmissões lado a lado -->
      <div class="top-charts">
        <div class="chart-container">
          <h2>Contagem de Flags</h2>
          <canvas ref="flagChartCanvas" width="300" height="250"></canvas>
        </div>

        <div class="chart-container">
          <h2>Contagem de Retransmissões</h2>
          <canvas ref="retransmissionChartCanvas" width="300" height="250"></canvas>
        </div>
      </div>

      <!-- Gráfico de tempo de resposta abaixo dos outros dois -->
      <div class="chart-container wide">
        <h2>Tempo de resposta: SIN e ACK</h2>
        <canvas ref="responseTimeChartCanvas" width="600" height="230"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'FlagCountChart',
  props: {
    packets: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      flagChart: null,
      retransmissionChart: null,
      responseTimeChart: null,
    };
  },
  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets && newPackets.data && newPackets.data.length > 0) {
          this.renderFlagChart();
          this.renderRetransmissionChart();
          this.renderResponseTimeChart();
        }
      },
      deep: true
    }
  },
  methods: {
    renderFlagChart() {
      const flags = this.countFlags(this.packets);

      if (this.flagChart) {
        this.flagChart.data.labels = Object.keys(flags);
        this.flagChart.data.datasets[0].data = Object.values(flags);
        this.flagChart.update();
      } else {
        const ctx = this.$refs.flagChartCanvas.getContext('2d');
        this.flagChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: Object.keys(flags),
            datasets: [{
              label: 'Contagem de Flags',
              data: Object.values(flags),
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
            scales: {
              y: {
                beginAtZero: true,
                stepSize: 1
              }
            }
          }
        });
      }
    },

    countFlags(packets) {
      const flags = {
        SYN: 0,
        ACK: 0,
        FIN: 0,
        RST: 0,
        PSH: 0,
        URG: 0
      };

      packets.data.forEach(packet => {
        if (packet.flags && packet.flags.length > 0) {
          packet.flags.forEach(flag => {
            if (Object.prototype.hasOwnProperty.call(flags, flag)) {
              flags[flag]++;
            }
          });
        }
      });

      return flags;
    },

    renderRetransmissionChart() {
      const retransmissions = this.countRetransmissions(this.packets);

      if (this.retransmissionChart) {
        this.retransmissionChart.data.labels = Object.keys(retransmissions);
        this.retransmissionChart.data.datasets[0].data = Object.values(retransmissions);
        this.retransmissionChart.update();
      } else {
        const ctx = this.$refs.retransmissionChartCanvas.getContext('2d');
        this.retransmissionChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: Object.keys(retransmissions),
            datasets: [{
              label: 'Retransmissões',
              data: Object.values(retransmissions),
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
                stepSize: 1
              }
            }
          }
        });
      }
    },

    countRetransmissions(packets) {
      let retransmissions = 0;

      packets.data.forEach(packet => {
        if (packet.flags && packet.flags.includes('RST')) {
          retransmissions++;
        }
      });

      return { Retransmissões: retransmissions };
    },

    renderResponseTimeChart() {
      const responseTimes = this.calculateResponseTimes(this.packets);

      if (this.responseTimeChart) {
        this.responseTimeChart.data.labels = Object.keys(responseTimes);
        this.responseTimeChart.data.datasets[0].data = Object.values(responseTimes);
        this.responseTimeChart.update();
      } else {
        const ctx = this.$refs.responseTimeChartCanvas.getContext('2d');
        this.responseTimeChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: Object.keys(responseTimes),
            datasets: [{
              label: 'Tempo de Resposta Médio (ms)',
              data: Object.values(responseTimes),
              backgroundColor: 'rgba(153, 102, 255, 0.6)',
              borderColor: 'rgba(153, 102, 255, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
                suggestedMin: 0,
              }
            }
          }
        });
      }
    },

    calculateResponseTimes(packets) {
      // const responseTimes = {};
      const ipPairs = {};

      packets.data.forEach(packet => {
        const ipOrigem = packet.ip_origem;
        const ipDestino = packet.ip_destino;
        const timestamp = packet.timestamp;

        // Criar chaves únicas para cada par de IPs (origem, destino)
        const key = `${ipOrigem}-${ipDestino}`;

        if (!ipPairs[key]) {
          ipPairs[key] = [];
        }
        ipPairs[key].push(timestamp);
      });

      const averageResponseTimes = {};

      Object.keys(ipPairs).forEach(key => {
        const timestamps = ipPairs[key];
        const total = timestamps.reduce((sum, timestamp, index) => {
          return index === timestamps.length - 1 ? sum : sum + (timestamps[index + 1] - timestamp);
        }, 0);

        // Calcular o tempo médio de resposta para o par de IPs
        averageResponseTimes[key] = total / (timestamps.length - 1);
      });

      return averageResponseTimes;
    },
  }
};
</script>

<style scoped>
.central-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.flag-count-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.top-charts {
  display: flex;
  justify-content: center;
  width: 100%;
  max-width: 1200px;
}

.chart-container {
  width: 45%;
  height: 500px;
  margin-bottom: 10px;
}

.chart-container.wide {
  width: 90%;
  margin: 60px 10px 10px;
}
</style>
