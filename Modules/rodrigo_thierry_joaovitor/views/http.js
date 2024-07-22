

fetch("http://localhost:3001/grupo_rodrigo_thierry_joao/http/info")
    .then(resp => resp.json())
    .then(json => {
        const data = json.Responses.reduce((acc, response) => {
            const contentType = response['Content-Type'];
            const contentLength = parseInt(response['Content-Length'], 10);

            if (!acc[contentType]) {
                acc[contentType] = {count: 0, totalLength: 0};
            }

            acc[contentType].count += 1;
            acc[contentType].totalLength += contentLength;

            return acc;
        }, {});


        const categories = Object.keys(data);
        const counts = categories.map(category => data[category].count);
        const totalLengths = categories.map(category => data[category].totalLength);
var option1;
option1 = {
    title: {
        text: 'Content-Type vs Volume de Dados',
        subtext: 'Número de ocorrências e volume de dados total por tipo de conteúdo',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['Número de Ocorrências', 'Volume de Dados Total'],
        left: 'left',
        top: 'bottom',

    },
    xAxis: {
        type: 'category',
        data: categories
    },
    yAxis: [
        {
            type: 'value',
            name: 'Número de Ocorrências',
            position: 'left'
        },
        {
            type: 'value',
            name: 'Volume de Dados Total (bytes)',
            position: 'right'
        }
    ],
    series: [
        {
            name: 'Número de Ocorrências',
            type: 'bar',
            data: counts
        },
        {
            name: 'Volume de Dados Total',
            type: 'bar',
            yAxisIndex: 1,
            data: totalLengths
        }
    ]
};


        const jsonRequests = json.Requests

        const methodData = jsonRequests.reduce((acc, request) => {
            const method = request.Method;

            if (!acc[method]) {
                acc[method] = 0;
            }

            acc[method] += 1;

            return acc;
        }, {});

        const methodNames = Object.keys(methodData);
        const methodCounts = methodNames.map(method => ({value: methodData[method], name: method}));

        
        option2 = {
    title: {
        text: 'Métodos de Requisição',
        subtext: 'Distribuição dos métodos de requisição HTTP',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        left: 'bottom'
    },
    legend: {
        orient: 'vertical',
        top: 'bottom',
        left: 'left',
        data: methodNames
    },
    series: [
        {
            name: 'Métodos de Requisição',
            type: 'pie',
            radius: '50%',
            data: methodCounts,
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

        

        var chartDom = document.getElementById('chart');
        var myChart = echarts.init(chartDom);
        option1 && myChart.setOption(option1);


        var chartDom = document.getElementById('pieChart');
        var myChart = echarts.init(chartDom);
        option2 && myChart.setOption(option2);


    })
    .then(json => {
        json.Responses.forEach((element) => {
            HTMLE
            }
        )
    })


