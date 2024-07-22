async function fetchARPData() {
  try {
    const response = await fetch("http://localhost:3001/trabalho2"); // Endpoint do backend
    const data = await response.json();
    for (let manufacturer in data.arp_data_by_manufacturer) {
      createPieChart(data.arp_data_by_manufacturer[manufacturer], manufacturer);
    }
  } catch (error) {
    console.error("Erro ao buscar dados ARP:", error);
  }
}

// Função para criar o gráfico de pizza com request e reply de um fabricante
function createPieChart(data, title) {
  console.log(data);
  let divChart = document.createElement("div");
  divChart.className = "chart";
  document.body.appendChild(divChart);
  let titleChart = document.createElement("h2");
  titleChart.innerText = title;
  divChart.appendChild(titleChart);
  let chartDom = document.createElement("div");
  chartDom.style.width = "600px";
  chartDom.style.height = "400px";
  divChart.appendChild(chartDom);

  var myChart = echarts.init(chartDom);
  var option = {
    title: {
      text: titleChart.innerText,
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
        name: "ARP",
        type: "pie",
        radius: "50%",
        data: [
          { value: data.requests, name: "Requests" },
          { value: data.replies, name: "Replies" },
        ],
      },
    ],
  };
  myChart.setOption(option);
}
fetchARPData(); // Busca os dados de ARP
