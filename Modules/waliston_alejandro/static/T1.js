const initCharts = async () => {
  const chart1 = echarts.init(document.getElementById("chart1"));
  const chart2 = echarts.init(document.getElementById("chart2"));
  const chart3 = echarts.init(document.getElementById("chart3"));
  const chart5 = echarts.init(document.getElementById("chart5"));
  const chart6 = echarts.init(document.getElementById("chart6"));
  const chart7 = echarts.init(document.getElementById("chart7"));
  const chart8 = echarts.init(document.getElementById("chart8"));
  const chart9 = echarts.init(document.getElementById("chart9"));

  const responseRip = await fetch("http://127.0.0.1:5000/api/rip/data");
  const dataRip = await responseRip.json();

  const dataRipBody = document.getElementById("dataRipBody");
    dataRip.forEach(item => {
      const row = document.createElement("tr");
      const roteador = document.createElement("td");
      roteador.textContent = item[0]; // Supondo que o roteador esteja no índice 0
      const endereco = document.createElement("td");
      endereco.textContent = item[1]; // Endereço no índice 1
      const distancia = document.createElement("td");
      distancia.textContent = item[2]; // Distância no índice 2
      const mascara = document.createElement("td");
      mascara.textContent = item[3]; // Máscara no índice 3
      const nextHop = document.createElement("td");
      nextHop.textContent = item[4]; // Next Hop no índice 4

      row.appendChild(roteador);
      row.appendChild(endereco);
      row.appendChild(distancia);
      row.appendChild(mascara);
      row.appendChild(nextHop);
      dataRipBody.appendChild(row);
  });

  // Dados reais (substitua pelos seus dados)
  const responseOrigem = await fetch("http://127.0.0.1:5000/api/origem/data");
  const dataOrigem = await responseOrigem.json();
  console.log(dataOrigem);

  const responseDestino = await fetch("http://127.0.0.1:5000/api/destino/data");
  const dataDestino = await responseDestino.json();

  const responseArp = await fetch("http://127.0.0.1:5000/api/arp/data");
  const dataArp = await responseArp.json();

  const responseUdp = await fetch("http://127.0.0.1:5000/api/udp/data");
  const dataUdp = await responseUdp.json();

  const responseTcp = await fetch("http://127.0.0.1:5000/api/tcp/data");
  const dataTcp = await responseTcp.json();
  console.log(dataTcp);

  const responseHttp = await fetch("http://127.0.0.1:5000/api/http/data");
  const dataHttp = await responseHttp.json();

  const responseDns = await fetch("http://127.0.0.1:5000/api/dns/data");
  const dataDns = await responseDns.json();

  const responseSnmp = await fetch("http://127.0.0.1:5000/api/snmp/data");
  const dataSnmp = await responseSnmp.json();


  
  

  const opcoesChart1 = {
    title: {
      text: 'TOP 10 endereços IP de Origem',
      left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line'
      }
    },
    xAxis: {
      type: "category",
      data: dataOrigem.map((item) => item[0]),
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "Repetições",
        type: "bar",
        data: dataOrigem.map((item) => item[1]),
      },
    ],
  };

  const opcoesChart2 = {
    title: {
      text: 'TOP 10 endereços IP de Destino',
      left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line'
      }
    },
    xAxis: {
      type: "category",
      data: dataDestino.map((item) => item[0]),
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "Repetições",
        type: "bar",
        data: dataDestino.map((item) => item[1]),
      },
    ],
  };

  const opcoesChart3 = {
    title: {
      text: 'Top 8 pares enderço IP e MAC que mais se comunicam entre si',
      left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line'
      }
    },
    xAxis: {
      type: "category",
      data: dataArp.map((item) => item[0] + "\n" + item[1]),
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "Repetições",
        type: "bar",
        data: dataArp.map((item) => item[2]),
      },
    ],
  };

  const opcoesChart5 = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 40,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: dataUdp.map((item) => ({
          name: item[0],
          value: item[1]
        })),
      },
    ],
  };

  const opcoesChart6 = {
    title: {
        text: 'Contagem de Pacotes TCP ao Longo do Tempo',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line'
        }
    },
    xAxis: {
        type: "category",
        data: dataTcp.map((item) => item[0].toFixed(2)), // Formatar o tempo
    },
    yAxis: {
        type: "value",
    },
    series: [
        {
            name: "Repetições",
            type: "line", // Alterar para 'line' para gráfico de área
            areaStyle: {}, // Adiciona estilo de área
            data: dataTcp.map((item) => item[1]),
        },
    ],
  };

  const opcoesChart7 = {
    title: {
      text: 'Métodos HTTP',
      left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line'
      }
    },
    xAxis: {
      type: "category",
      data: dataHttp.map((item) => item[0]),
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "Repetições",
        type: "bar",
        data: dataHttp.map((item) => item[1]),
      },
    ],
  };


  const opcoesChart8 = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 40,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: dataDns.map((item) => ({
          name: item[0],
          value: item[1]
        })),
      },
    ],
  };

  const opcoesChart9 = {
    title: {
      text: 'Tipos de PDUs',
      left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line'
      }
    },
    xAxis: {
      type: "category",
      boundaryGap: true,
      data: dataSnmp.map((item) => item[0]),
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "Repetições",
        type: "bar",
        data: dataSnmp.map((item) => item[1]),
      },
    ],
  };

  chart1.setOption(opcoesChart1);
  chart2.setOption(opcoesChart2);
  chart3.setOption(opcoesChart3);
  chart5.setOption(opcoesChart5);
  chart6.setOption(opcoesChart6);
  chart7.setOption(opcoesChart7);
  chart8.setOption(opcoesChart8);
  chart9.setOption(opcoesChart9);

};

export default initCharts;
