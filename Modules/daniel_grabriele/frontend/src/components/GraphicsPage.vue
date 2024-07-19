<template>
  <div class="chart-container">
    <!-- Gráfico de IP de Origem -->
    <div class="chart">
      <h2 class="chart-title">Ocorrências de IP de Origem</h2>
      <canvas id="grafico-ip-origem" width="300px" height="200px"></canvas>
    </div>

    <!-- Gráfico de IP de Destino -->
    <div class="chart">
      <h2 class="chart-title">Ocorrências de IP de Destino</h2>
      <canvas id="grafico-ip-destino" width="300px" height="200px"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart } from "chart.js";

export default {
  name: 'GraphicsPage',
  props: {
    packets: {
      type: Number,
      data: Array
    }
  },
  mounted() {
    this.createGraphicsIPV4();
  },  
  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets.data.length > 0 && newPackets.type == 0) {
          this.atualizarGraficosIPV4(); 
        }
      },
      deep: true
    }
  },
  methods: {
    createGraphicsIPV4(){
      // Extrai os endereços IP de origem e destino dos pacotes
      const ipsOrigem = this.packets.data.map(pacote => pacote.ip_origem);
      const ipsDestino = this.packets.data.map(pacote => pacote.ip_destino);

      // Conta a ocorrência de cada endereço IP
      const contadorOrigem = this.contarOcorrencias(ipsOrigem);
      const contadorDestino = this.contarOcorrencias(ipsDestino);

      // Dados do gráfico de IP de origem
      const dataOrigem = {
        labels: Object.keys(contadorOrigem),
        datasets: [{
          label: 'IP de Origem',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
          data: Object.values(contadorOrigem)
        }]
      };

      // Dados do gráfico de IP de destino
      const dataDestino = {
        labels: Object.keys(contadorDestino),
        datasets: [{
          label: 'IP de Destino',
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          data: Object.values(contadorDestino)
        }]
      };

      // Opções dos gráficos
      const options = {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      };

      // Renderiza o gráfico de IP de origem
      const ctxOrigem = document.getElementById('grafico-ip-origem').getContext('2d');
      this.chartOrigem = new Chart(ctxOrigem, {
        type: 'bar',
        data: dataOrigem,
        options: options
      });

      // Renderiza o gráfico de IP de destino
      const ctxDestino = document.getElementById('grafico-ip-destino').getContext('2d');
      this.chartDestino = new Chart(ctxDestino, {
        type: 'bar',
        data: dataDestino,
        options: options
      });

    },
    criarGraficoIP() {
      if(this.packets.type == 0){
        this.createGraphicsIPV4();
      }
    },
    contarOcorrencias(arr) {
      return arr.reduce((acc, curr) => {
        acc[curr] ? acc[curr]++ : (acc[curr] = 1);
        return acc;
      }, {});
    },
    atualizarGraficosIPV4() {
      // Atualiza os gráficos com os novos dados
      console.log(this.packets.data)
      const ipsOrigem = this.packets.data.map(pacote => pacote.ip_origem);
      const ipsDestino = this.packets.data.map(pacote => pacote.ip_destino);

      const contadorOrigem = this.contarOcorrencias(ipsOrigem);
      const contadorDestino = this.contarOcorrencias(ipsDestino);

      // Atualiza os dados do gráfico de IP de origem
      this.chartOrigem.data.labels = Object.keys(contadorOrigem);
      this.chartOrigem.data.datasets[0].data = Object.values(contadorOrigem);
      this.chartOrigem.update();

      // Atualiza os dados do gráfico de IP de destino
      this.chartDestino.data.labels = Object.keys(contadorDestino);
      this.chartDestino.data.datasets[0].data = Object.values(contadorDestino);
      this.chartDestino.update();
    }
  }
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
}

.chart {
  margin-bottom: 50px;
  width: 80%;
}

.chart-title {
  text-align: center;
  margin-top: 10px;
  font-size: 16px;
  color: #333;
  text-transform: uppercase;
}
</style>