
const apiResponse = fetch("http://localhost:3001/grupo_rodrigo_thierry_joao/udp/sugestaoDeivis")
    .then(response => response.json())
    .then(data => {
        // Preparar dados para ECharts
        const ports = Object.keys(data.n_req);
        const requestCounts = Object.values(data.n_req);
        const dataAmounts = ports.map(port => data.data[port] || 0);

        // Função para obter a descrição do serviço para uma porta específica
        function getServiceDescription(port) {
            return fetch(`http://localhost:3001/grupo_rodrigo_thierry_joao/udp/services/${port}`)
                .then(response => response.json())
                .then(serviceData => serviceData[0]?.description || 'Unknown Service');
        }

        // Obter descrições de serviços para todas as portas
        const portDescriptions = {};
        const promises = ports.map(port => {
            return getServiceDescription(port).then(description => {
                portDescriptions[port] = description;
            });
        });

        Promise.all(promises).then(() => {
            // Configurar e renderizar gráficos ECharts após obter as descrições
            const requestChart = echarts.init(document.getElementById('requestChart'));
            const dataChart = echarts.init(document.getElementById('dataChart'));

            const requestOption = {
                title: {
                    text: 'Número de requisições recebidas por porta'
                },
                tooltip: {},
                xAxis: {
                    type: 'category',
                    data: ports.map(port => `${port} (${portDescriptions[port]})`)
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    name: 'Requisições',
                    type: 'bar',
                    data: requestCounts
                }]
            };

            const dataOption = {
                title: {
                    text: 'Volume de tráfego gerado por porta (Bytes)'
                },
                tooltip: {},
                xAxis: {
                    type: 'category',
                    data: ports.map(port => `${port} (${portDescriptions[port]})`)
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    name: 'Data Amount',
                    type: 'bar',
                    data: dataAmounts
                }]
            };

            requestChart.setOption(requestOption);
            dataChart.setOption(dataOption);
        });
    })
    .catch(error => console.error('Error fetching API data:', error));


/// Não mais usado
/*
var chartDom = document.getElementById('graph');

var myChart = echarts.init(chartDom);
var option;

myChart.showLoading();
$.getJSON('http://127.0.0.1:3001/grupo_rodrigo_thierry_joao/udp/graph', function (graph) {
    myChart.hideLoading();
    graph.nodes.forEach(function (node) {
        node.label = {
            show: node.symbolSize > 30
        };
    });
    option = {
        title: {
            text: '______',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right'
        },
        tooltip: {},
        legend: [
            {
                // selectedMode: 'single',
                data: graph.categories.map(function (a) {
                    return a.name;
                })
            }
        ],
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
            {
                edgeSymbol: ['circle', 'arrow'],
                name: 'Tráfico UDP',
                type: 'graph',
                legendHoverLink: false,
                layout: 'circular',
                data: graph.nodes,
                links: graph.links,
                categories: graph.categories,
                roam: true,
                label: {
                    position: 'right',
                    formatter: '{b}'
                },
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                },
                emphasis: {
                    focus: 'adjacency',
                    lineStyle: {
                        width: 10
                    }
                }
            }
        ]
    };
    myChart.setOption(option);
});

option && myChart.setOption(option);
 */