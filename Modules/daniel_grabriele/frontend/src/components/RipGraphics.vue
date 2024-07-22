<template>
  <div class="chart-container">
    <div class="chart-wrapper">
      <h2>Gráficos de Comandos RIP</h2>
      <canvas ref="ripChart"></canvas>
    </div>
    <div class="chart-wrapper">
      <h2>Gráfico de Métricas de Rotas</h2>
      <canvas ref="metricChart"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: {
    packets: {
      type: Object,
    }
  },
  data() {
    return {
      ripChart: null,
      metricChart: null,
      ipChart: null
    };
  },
  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets && newPackets.data && newPackets.data.length > 0) {
          this.renderRipChart(newPackets);
          this.renderMetricChart(newPackets);
        }
      },
      deep: true
    }
  },
  methods: {
    renderRipChart(packets) {
      const ripCounts = this.countRipCommands(packets);

      if (this.ripChart) {
        this.ripChart.data.labels = Object.keys(ripCounts);
        this.ripChart.data.datasets[0].data = Object.values(ripCounts);
        this.ripChart.update();
      } else {
        const ctx = this.$refs.ripChart.getContext('2d');
        this.ripChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: Object.keys(ripCounts),
            datasets: [{
              label: 'Contagem de Pacotes RIP por Tipo de Comando',
              data: Object.values(ripCounts),
              backgroundColor: [
                'rgba(54, 162, 235, 0.5)', // Azul claro
                'rgba(255, 99, 132, 0.5)'  // Vermelho claro
              ],
              borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    },

    renderMetricChart(packets) {
      const metrics = this.countMetrics(packets);

      if (this.metricChart) {
        this.metricChart.data.labels = metrics.timestamps;
        this.metricChart.data.datasets[0].data = metrics.values;
        this.metricChart.data.datasets[0].backgroundColor = metrics.colors;
        this.metricChart.update();
      } else {
        const ctx = this.$refs.metricChart.getContext('2d');
        this.metricChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: metrics.timestamps,
            datasets: [{
              label: 'Métrica de Rotas ao Longo do Tempo',
              data: metrics.values,
              backgroundColor: metrics.colors,
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    },

    countRipCommands(packets) {
      const ripCounts = {
        Request: 0,
        Response: 0
      };

      packets.data.forEach(packet => {
        if (packet.command_type === 'Request') {
          ripCounts.Request++;
        } else if (packet.command_type === 'Response') {
          ripCounts.Response++;
        }
      });

      return ripCounts;
    },

    countMetrics(packets) {
      const timestamps = [];
      const values = [];
      const colors = [];

      packets.data.forEach(packet => {
        packet.entries.forEach(entry => {
          timestamps.push(new Date(packet.timestamp * 1000).toLocaleTimeString());
          values.push(entry.metric);
          colors.push(entry.metric === 16 ? 'rgba(255, 99, 132, 0.5)' : 'rgba(75, 192, 192, 0.5)');
        });
      });

      return { timestamps, values, colors };
    },

  }
};
</script>

<style>
.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-wrapper {
  width: 60%;
  margin-bottom: 20px;
}

canvas {
  width: 100%;
  margin: 10px 0;
}

.small-chart {
  height: 200px; 
}

h2 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
