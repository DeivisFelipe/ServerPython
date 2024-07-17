function transformToTree(data) {
    function createNode(name, data, parentName) {
        fullname = parentName;
        let node = {
            name: name,
            fullname: fullname,
            children: []
        };
        for (let key in data) {
            node.children.push(createNode(key, data[key], fullname));
        }
        return node;
    }
    
    return createNode('', data, '');
}


let root;
function createTreeList(node, parentElement) {
    let li = document.createElement('li');
    li.textContent = node.name;
    li.title = node.fullname;
    li.className = 'MYli';

    li.onclick = function(event) {
        event.stopPropagation();
        let children = li.querySelector('ul');
        if (children) {
            children.style.display = children.style.display === 'none' ? 'block' : 'none';
        }
    };

    if (node.children.length > 0) {
        let ul = document.createElement('ul');
        ul.className = 'MYul';
        node.children.forEach(child => createTreeList(child, ul));
        li.appendChild(ul);
    }
    
    parentElement.appendChild(li);
}


fetch('http://localhost:3001/grupo_rodrigo_thierry_joao/snmp/tree')
    .then(response => response.json())
    .then(data => {
        const treeData = transformToTree(data);
        var container = document.getElementById('graphContainer');
        container.innerHTML = '';

        var ul = document.createElement('ul');
        ul.className = 'MYul';
        createTreeList(treeData, ul);
        container.appendChild(ul);
    })
    .catch(error => console.error('Error fetching or transforming data:', error));
