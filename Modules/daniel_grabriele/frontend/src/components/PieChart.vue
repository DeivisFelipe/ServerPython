<template>
  <div class="pie-chart">
    <h3>{{ title }}</h3>
    <canvas ref="pieChart"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'PieChart',
  props: {
    chartData: Object,
    title: String
  },
  mounted() {
    this.renderPieChart();
  },
  methods: {
    renderPieChart() {
      const canvas = this.$refs.pieChart;
      if (!canvas) return;

      const ctx = canvas.getContext('2d');

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: this.chartData.labels,
          datasets: [{
            label: 'DNS Queries',
            data: this.chartData.data,
            backgroundColor: this.chartData.colors,
            borderColor: this.chartData.colors.map(color => color.replace('0.6', '1')),
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              callbacks: {
                label: function(tooltipItem) {
                  return `${tooltipItem.label}: ${tooltipItem.raw}`;
                }
              }
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.pie-chart {
  width: 30%;
  margin: 1%;
}

h3 {
  text-align: center;
}
</style>
