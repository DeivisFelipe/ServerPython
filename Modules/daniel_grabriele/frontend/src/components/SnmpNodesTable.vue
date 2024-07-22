<template>
  <div class="snmp-nodes-table">
    <h2>Lista de Informações: Protocolo SNMP</h2>
    <table>
      <thead>
        <tr>
          <th>Número do Pacote</th>
          <th>Timestamp</th>
          <th>Comando</th>
          <th>Dados</th>
          <th>IP de Origem</th>
          <th>IP de Destino</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(entry, index) in snmpEntries" :key="index">
          <td>{{ index + 1 }}</td>
          <td>{{ entry.timestamp }}</td>
          <td>{{ entry.comando }}</td>
          <td>{{ entry.dados }}</td>
          <td>{{ entry.source_ip }}</td>
          <td>{{ entry.destination_ip }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    snmpNodes: {
      type: Array,
      required: true
    }
  },
  computed: {
    snmpEntries() {
      if (!this.snmpNodes || this.snmpNodes.length === 0) {
        return [];
      }

      const seenEntries = new Set();
      const uniqueEntries = [];

      this.snmpNodes.forEach(node => {
        const key = `${node.timestamp}_${node.comando}_${node.dados}_${node.ip_origem}_${node.ip_destino}`;

        if (!seenEntries.has(key)) {
          seenEntries.add(key);
          uniqueEntries.push({
            timestamp: node.timestamp,
            comando: node.comando,
            dados: node.dados,
            source_ip: node.ip_origem,
            destination_ip: node.ip_destino
          });
        }
      });
      return uniqueEntries;
    }
  }
};
</script>

<style scoped>
.snmp-nodes-table {
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
