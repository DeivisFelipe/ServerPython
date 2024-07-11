function transformToTree(data) {
    const transform = (obj) => {
        return Object.keys(obj).map(key => ({
            name: key,
            children: transform(obj[key])
        }));
    };
    return {
        name: 'Root',
        children: transform(data)
    };
}

fetch('http://localhost:3001/grupo_rodrigo_thierry_joao/snmp/oids')
    .then(response => response.json())
    .then(data => {
        const treeData = transformToTree(data);

        const mychart = echarts.init(document.getElementById('graphContainer'));

        const option = {
            tooltip: {
                trigger: 'item',
                triggerOn: 'mousemove'
            },
            series: [
                {
                    type: 'tree',
                    data: [treeData],
                    top: '1%',
                    left: '7%',
                    bottom: '1%',
                    right: '20%',
                    symbolSize: 7,
                    label: {
                        position: 'left',
                        verticalAlign: 'middle',
                        align: 'right',
                        fontSize: 9
                    },
                    leaves: {
                        label: {
                            position: 'right',
                            verticalAlign: 'middle',
                            align: 'left'
                        }
                    },
                    expandAndCollapse: true,
                    animationDuration: 550,
                    animationDurationUpdate: 750
                }
            ]
        };

        mychart.setOption(option);
    })
    .catch(error => console.error('Error fetching or transforming data:', error));
