<template>
  <div class="http-details">
    <h2>Lista de Pacotes HTTP</h2>
    <table>
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>IP de Origem</th>
          <th>IP de Destino</th>
          <th>Método HTTP</th>
          <th>URI</th>
          <th>Versão HTTP</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(request, index) in requests" :key="index">
          <td>{{ new Date(request.timestamp * 1000).toLocaleString() }}</td>
          <td>{{ request.ip_origem }}</td>
          <td>{{ request.ip_destino }}</td>
          <td>{{ request.metodo }}</td>
          <td>{{ request.uri }}</td>
          <td>{{ request.versao }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    requests: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
.http-details {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

ul {
  margin: 0;
  padding: 0;
  list-style-type: none;
}

ul li {
  margin-bottom: 4px;
}
</style>
