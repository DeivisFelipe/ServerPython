async function fetchData() {
    const response = await fetch(`http://localhost:3001/trabalho7`);
    const data = await response.json();

    let sites = document.getElementById('sites');
    for(let i = 0; i < 10; i++) {
        let row  = document.createElement('p');
        row.innerHTML = i+ '. Site:' + data[i][0] + ' - Acessos: ' + data[i][1] + ' acessos';
        sites.appendChild(row);
    }
}

fetchData();