async function fetchT3() {
  try {
    const response = await fetch("http://localhost:3001/trabalho3"); // Endpoint do backend
    const data = await response.json();
    let totalPacotes = document.getElementById("totalPacotes");
    totalPacotes.innerText = data.total_packets;
    //cria chart para rotas e a quantidade por rota
    createPieChart(data.routers, "originIp",'Roteadores');
    //cria chart para request e response
    //cria um json com a quantidade de request e response
    console.log("123");
    let grafico2 = {
      request: data.request_packets,
      response: data.response_packets,
    };
    createPieChart(grafico2, "reqRes",'Request e Response');
  } catch (error) {
    console.error("Erro ao buscar dados :", error);
  }
}

// Função para criar o gráfico de pizza
function createPieChart(data, idChart,title) {
  let chartDom = document.getElementById(idChart);
  console.log(data);
  let labels = Object.keys(data);
  let values = Object.values(data);
  var myChart = echarts.init(chartDom);
  var option = {
    title: {
      text: title,
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
        name: idChart,
        type: "pie",
        radius: "50%",
        data: values.map((value, index) => {
          return { value: value, name: labels[index] };
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
  myChart.setOption(option);
}
fetchT3();
