// PREENCHER SELECTS
document.addEventListener('DOMContentLoaded', function () {
    const url = 'http://localhost:3001/grupo_rodrigo_thierry_joao/http/';

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ipv4Select = document.getElementById('ipv4_selectc');
            ipv4Select.innerHTML = ''; // Clear any existing options

            data.forEach(ipv4 => {
                const option = document.createElement('option');
                option.value = ipv4.toString().replace(",", " <-> ");
                option.textContent = option.value;
                ipv4Select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Failed to fetch IPv4 addresses.', error);
        });
});

//ECHARTS


// Calculate the time offsets
function calculateTimeOffsets(timestamps) {
    const startTime = Math.min(...timestamps);
    return timestamps.map(ts => ts - startTime);
}


async function fetchService(port) {
    try {
        const response = await fetch(`http://localhost:3001/grupo_rodrigo_thierry_joao/udp/services/${port}`)
            .then(text => text.json());


        return response[0].description;
    } catch (error) {
        console.error(`Error fetching service for port ${port}:`, error);
        return 'Unknown';
    }
}

async function buildTable(data) {
    const tableBody = document.getElementById('ports_table_body');
    tableBody.innerHTML = ""
    const seen = new Set();

    for (const [ip, info] of Object.entries(data)) {
        for (const [srcPort, dstPort] of info.bind) {
            const key = `${ip}-${srcPort}-${dstPort}`;
            if (seen.has(key)) continue;

            seen.add(key);
            const service = await fetchService(dstPort);

            const row = document.createElement('tr');

            const ipCell = document.createElement('td');
            ipCell.textContent = ip;
            row.appendChild(ipCell);

            const srcPortCell = document.createElement('td');
            srcPortCell.textContent = srcPort;
            row.appendChild(srcPortCell);

            const dstPortCell = document.createElement('td');
            dstPortCell.textContent = dstPort;
            row.appendChild(dstPortCell);

            const serviceCell = document.createElement('td');
            serviceCell.textContent = service;
            row.appendChild(serviceCell);

            tableBody.appendChild(row);
        }
    }
}


function submiter() {

    let ips = document.getElementById("ipv4_selectc").value.split(" <-> ");


    let url = `http://localhost:3001/grupo_rodrigo_thierry_joao/tcp/info/`
        + `${ips[0]}/`
        + `-1/`
        //+`${document.getElementById("porta_origem").value}/`
        + `${ips[1]}/`
        + `-1/`
    //+`${document.getElementById("porta_destino").value}`

    console.log(url)

    fetch(url)
        .then(response => response.json())
        .then(data => {
            var ips = Object.keys(data);
            // Número de pacotes
            var n_pkt_chart = echarts.init(document.getElementById('n_pkt_chart'));
            var n_pkt_option = {
                title: {
                    text: 'Número de Pacotes',
                    left: 'center',
                    top: '10%'  // Ajustar a posição do título
                },
                tooltip: {},
                xAxis: {
                    type: 'category',
                    data: ips
                },
                yAxis: {
                    type: 'value'
                },
                legend: {
                    show: false  // Ocultar a legenda
                },
                series: [{
                    name: 'Pacotes',
                    type: 'bar',
                    data: ips.map(ip => data[ip].n_pkt)
                }]
            };
            n_pkt_chart.setOption(n_pkt_option);

            // Tamanho da Janela ao longo do tempo
            var w_size_chart = echarts.init(document.getElementById('w_size_chart'));
            var w_size_option = {
                title: {
                    text: 'Tamanho da Janela ao Longo do Tempo\n'
                },
                tooltip: {},
                legend: {
                    data: ips,
                    top: 'bottom'
                },
                xAxis: {
                    type: 'value',
                    name: 'Time (s)'
                },
                yAxis: {
                    type: 'value'
                },
                series: ips.map(ip => ({
                    name: ip,
                    type: 'line',
                    data: calculateTimeOffsets(data[ip].timestamp).map((time, index) => [time, data[ip].w_size[index]])
                }))
            };
            w_size_chart.setOption(w_size_option);

            // Tamanho do Payload ao longo do tempo
            var payload_size_chart = echarts.init(document.getElementById('payload_size_chart'));
            var payload_size_option = {
                title: {
                    text: 'Tamanho de Payload ao Longo do Tempo'
                },
                tooltip: {},
                legend: {
                    data: ips,
                    top: 'bottom'
                },
                xAxis: {
                    type: 'value',
                    name: 'Tempo (s)'
                },
                yAxis: {
                    type: 'value'
                },
                series: ips.map(ip => ({
                    name: ip,
                    type: 'line',
                    data: calculateTimeOffsets(data[ip].timestamp).map((time, index) => [time, data[ip].payload_size[index]])
                }))
            };
            payload_size_chart.setOption(payload_size_option);

            buildTable(data);
        })

    return false;
}

