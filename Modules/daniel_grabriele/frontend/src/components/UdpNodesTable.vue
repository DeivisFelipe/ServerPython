<template>
  <div class="udp-nodes-table">
    <h2>Lista de Informações: Protocolo UDP</h2>
    <table>
      <thead>
        <tr>
          <th>Endereço IP de Origem</th>
          <th>Endereço IP de Destino</th>
          <th>Porta de Origem</th>
          <th>Porta de Destino</th>
          <th>Comprimento</th>
          <th>Checksum</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(entry, index) in udpEntries" :key="index">
          <td>{{ entry.source_ip }}</td>
          <td>{{ entry.destination_ip }}</td>
          <td>{{ entry.source_port }}</td>
          <td>{{ entry.destination_port }}</td>
          <td>{{ entry.length }}</td>
          <td>{{ entry.checksum }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    udpNodes: {
      type: Array,
      required: true
    }
  },
  computed: {
    udpEntries() {
      if (!this.udpNodes || this.udpNodes.length === 0) {
        return [];
      }

      const seenEntries = new Set();
      const uniqueEntries = []; 

      this.udpNodes.forEach(node => {
        const key = `${node.source_ip}_${node.destination_ip}_${node.source_port}_${node.destination_port}_${node.length}_${node.checksum}`;

        if (!seenEntries.has(key)) {
          seenEntries.add(key);
          uniqueEntries.push({
            source_ip: node.ip_origem,
            destination_ip: node.ip_destino,
            source_port: node.porta_origem,
            destination_port: node.porta_destino,
            length: node.comprimento,
            checksum: node.checksum
          });
        }
      });
      return uniqueEntries;
    }
  }
};
</script>

<style scoped>
.udp-nodes-table {
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
