async function getT1Data() {
  try {
    const response = await fetch("http://localhost:3001/trabalho1"); // Endpoint do backend
    const data = await response.json();

    if (!data || !data) {
      console.error("Dados de ARP requests ou replies não encontrados.");
      return;
    }
    createPieChartTTL(data.ttl_dict); // Cria o gráfico de pizza com os dados gerais de ARP
  } catch (error) {
    console.error("Erro ao buscar dados ARP:", error);
  }
}

// Função para criar o gráfico de pizza com os dados gerais de ARP
function createPieChartTTL(data) {
  var chartDom = document.getElementById("ttl-chart");
  var myChart = echarts.init(chartDom);
  var option;

  var ttl_dict = data;
  var ttl_values = Object.values(ttl_dict);
  var ttl_keys = Object.keys(ttl_dict);

  option = {
    title: {
      text: "Resumo de TTL",
      subtext: "Distribuição de TTL",
      left: "center",
    },
    tooltip: {
      trigger: "item",
    },
    legend: {
      orient: "vertical",
      left: "left",
    },
    series: [
      {
        name: "TTL",
        type: "pie",
        radius: "50%",
        data: ttl_keys.map((key, index) => {
          return { value: ttl_values[index], name: key };
        }),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
        },
      },
    ],
  };

  option && myChart.setOption(option);
}

getT1Data();
