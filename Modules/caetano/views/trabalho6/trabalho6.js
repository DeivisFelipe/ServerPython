async function fetchHTTPData() {
    try {
        const response = await fetch('http://127.0.0.1:3001/trabalho6');  // Endpoint do backend
        const data = await response.json();
        createPieChart(data);
        let table = document.getElementById('table');
        data.http_packets.forEach((packet) => {
            let row  = document.createElement('tr');
            row.innerHTML = `
                <td>${packet.src_ip}</td>
                <td>${packet.dst_ip}</td>
                <td>${packet.src_port}</td>
                <td>${packet.dst_port}</td>
            `;
            table.appendChild(row);
        }
        );
    } catch (error) {
        console.error('Erro ao buscar dados HTTP:', error);
    }
}
function createPieChart(data){
    var chartDom = document.getElementById('reqHttp');
    var myChart = echarts.init(chartDom);
    var option;
    let tiposRequisicaoKeys = Object.keys(data.http_methods);
    let tiposRequisicaoValues = Object.values(data.http_methods);
    option = {
        title: {
            text: 'Tipos de Requisição HTTP',
            subtext: 'Métodos de Requisição',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: 'Métodos',
                type: 'pie',
                radius: '50%',
                data: tiposRequisicaoKeys.map((key, index) => {
                    return { value: tiposRequisicaoValues[index], name: key };
                }),
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    option && myChart.setOption(option);
}
fetchHTTPData();
