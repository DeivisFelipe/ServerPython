<template>
  <div>
    <canvas ref="barChart"></canvas>
  </div>
</template>

<script>
import { Chart } from 'chart.js';

export default {
  name: 'HistogramAddress',
  props: {
    enderecosIP: Array
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const ctx = this.$refs.barChart.getContext('2d');

      // Contar as ocorrências de cada endereço IP
      const ipCounts = this.countIPOccurrences();

      // Dados para o gráfico
      const data = {
        labels: Object.keys(ipCounts), // Use IP addresses as labels
        datasets: [{
          label: 'Ocorrências de Endereços IP',
          data: Object.values(ipCounts), // Use counts as data
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      };

      // Opções do gráfico
      const options = {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0 // Garante que números inteiros sejam exibidos
            }
          }
        }
      };

      // Renderizar o gráfico de barras usando Chart.js
      new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: options
      });
    },
    countIPOccurrences() {
      const ipCounts = {};
      // Contar ocorrências de cada endereço IP
      this.enderecosIP.forEach(ip => {
        ipCounts[ip] = (ipCounts[ip] || 0) + 1;
      });
      return ipCounts;
    }
  }
};
</script>

<style>
/* Estilos opcionais */
</style>
