<template>
  <div class="rip-nodes-table">
    <h2>Lista de Informações: Protocolo RIP</h2>
    <table>
      <thead>
        <tr>
          <th>Endereço IP de Origem</th>
          <th>Endereço IP de Destino</th>
          <th>Tipo de Comando</th>
          <th>Versão</th>
          <th>Endereço IP</th>
          <th>Rótulo da Rota</th>
          <th>Próximo Salto</th>
          <th>Métrica</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(entry, index) in ripEntries" :key="index">
          <!-- Informações do cabeçalho RIP -->
          <td>{{ entry.source_ip }}</td>
          <td>{{ entry.destination_ip }}</td>
          <td>{{ entry.command_type }}</td>
          <td>{{ entry.version }}</td>
          
          <!-- Informações das entradas de rota RIP -->
          <td>{{ entry.ip_address }}</td>
          <td>{{ entry.route_tag }}</td>
          <td>{{ entry.next_hop }}</td>
          <td>{{ entry.metric }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    ripNodes: {
      type: Array,
      required: true
    }
  },
  computed: {
    ripEntries() {
      if (!this.ripNodes || this.ripNodes.length === 0) {
        return [];
      }

      const seenEntries = new Set();
      const uniqueEntries = []; 

      this.ripNodes.forEach(node => {
        node.entries.forEach(entry => {
          const key = `${node.source_ip}_${entry.ip_address}_${entry.route_tag}_${entry.next_hop}_${entry.metric}`;
          if (!seenEntries.has(key)) {
            seenEntries.add(key)
            uniqueEntries.push({
              timestamp: node.timestamp,
              source_ip: node.source_ip,
              destination_ip: node.destination_ip,
              command_type: node.command_type,
              version: node.version,
              ip_address: entry.ip_address,
              route_tag: entry.route_tag,
              next_hop: entry.next_hop,
              metric: entry.metric
            });
          }
        });
      });
      return uniqueEntries;
    }
  }
};
</script>

<style scoped>
.rip-nodes-table {
  width: 100%;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}
</style>
