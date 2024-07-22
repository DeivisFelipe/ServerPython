async function fetchData() {
    const response = await fetch(`http://localhost:3001/trabalho8`);
    const data = await response.json(); 
    createPieChart(data);
}
function createPieChart(data){
    var chartDom = document.getElementById("pduChart");
    console.log(data);

    var myChart = echarts.init(chartDom);
    var option;
    var data = data;
    var data_values = Object.values(data);
    var data_keys = Object.keys(data);
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
                data: data_keys.map((key, index) => {
                    return { value: data_values[index], name: key };
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

fetchData();