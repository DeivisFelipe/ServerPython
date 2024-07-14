document.addEventListener("DOMContentLoaded", function() {
    const packetCountSelect = document.getElementById('packet-count-select');
    const lengthOverTimeChartCanvas = document.getElementById('length-over-time-chart');
    const ipTrafficDistributionChartCanvas = document.getElementById('ip-traffic-distribution-chart');
    const ctx1 = lengthOverTimeChartCanvas.getContext('2d');
    const ctx3 = ipTrafficDistributionChartCanvas.getContext('2d');
    let chartInstance1 = null;
    let chartInstance3 = null;

    function updateLengthOverTimeChart(data) {
        const timestamps = [];
        const packetLengths = [];

        // Pegar a quantidade de pacotes selecionada
        let packetCount = packetCountSelect.value;
        if (packetCount === 'all') {
            packetCount = data.length; // Mostrar todos os pacotes
        } else {
            packetCount = parseInt(packetCount); // Converter para número inteiro
        }

        // Selecionar os últimos pacotes conforme a quantidade escolhida
        const selectedData = data.slice(-packetCount);

        selectedData.forEach(packet => {
            const timestamp = new Date(packet.time * 1000).toLocaleString();
            timestamps.push(timestamp);
            packetLengths.push(packet.length);
        });

        // Se já existir uma instância do gráfico, destruir antes de criar um novo
        if (chartInstance1) {
            chartInstance1.destroy();
        }

        // Gerar gráfico de linha
        chartInstance1 = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: timestamps,
                datasets: [{
                    label: 'Tamanho Médio dos Pacotes',
                    data: packetLengths,
                    borderColor: getRandomColor(),
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }

    function updateIpTrafficDistributionChart(data) {
        const ipTrafficLabels = {};
    
        // Contar ocorrências de cada par IP de Origem/Destino
        data.forEach(packet => {
            const ipPair = `${packet.source} > ${packet.destination}`;
            if (ipTrafficLabels[ipPair]) {
                ipTrafficLabels[ipPair]++;
            } else {
                ipTrafficLabels[ipPair] = 1;
            }
        });
    
        const labels = Object.keys(ipTrafficLabels);
        const dataCounts = Object.values(ipTrafficLabels);
    
        // Se já existir uma instância do gráfico, destruir antes de criar um novo
        if (chartInstance3) {
            chartInstance3.destroy();
        }
    
        // Gerar gráfico de área empilhada
        chartInstance3 = new Chart(ctx3, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Distribuição de Tráfego por IP de Origem/Destino',
                    data: dataCounts,
                    backgroundColor: labels.map(() => getRandomColor()),
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }

    fetch('http://localhost:3001/trabalho8')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById("packets-table-body");
            const timestamps = [];
            const packetLengths = [];
            let totalBytes = 0;

            data.forEach(packet => {
                const row = document.createElement("tr");
                const timestamp = new Date(packet.time * 1000).toLocaleString();
                timestamps.push(timestamp);
                packetLengths.push(packet.length);
                totalBytes += packet.length;

                row.innerHTML = `
                    <td>${packet.number}</td>
                    <td>${timestamp}</td>
                    <td>${packet.source}</td>
                    <td>${packet.destination}</td>
                    <td>${packet.protocol}</td>
                    <td>${packet.length}</td>
                    <td>${packet.info}</td>
                `;
                tbody.appendChild(row);
            });

            // Atualizar os gráficos inicialmente com todos os dados
            updateLengthOverTimeChart(data);
            updateIpTrafficDistributionChart(data);

            // Atualizar os gráficos quando o usuário mudar a seleção de pacotes
            packetCountSelect.addEventListener('change', function() {
                updateLengthOverTimeChart(data);
                updateIpTrafficDistributionChart(data);
            });

        })
        .catch(error => console.error('Error fetching data:', error));
});

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
