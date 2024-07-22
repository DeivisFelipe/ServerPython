<template>
  <div class="dns-packages-table">
    <h2>Lista de Pacotes DNS</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Endereço IP de Origem</th>
          <th>Endereço IP de Destino</th>
          <th>Queries</th>
          <th>Answers</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(packageGroup, id) in groupedPackages" :key="id">
          <td>{{ id }}</td>
          <td>{{ packageGroup.source_ip || 'N/A' }}</td>
          <td>{{ packageGroup.destination_ip || 'N/A' }}</td>
          <td>
            <ul>
              <li v-for="(query, index) in packageGroup.queries" :key="index">
                {{ query.name }} (Type: {{ query.type }}, Class: {{ query.class }})
              </li>
            </ul>
          </td>
          <td>
            <ul>
              <li v-for="(answer, index) in packageGroup.answers" :key="index">
                {{ answer.name }} (Type: {{ answer.type }}, Class: {{ answer.class }}, TTL: {{ answer.ttl }}, RDATA: {{ answer.rdata }})
              </li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    dnsPackages: {
      type: Array,
      required: true
    }
  },
  computed: {
    groupedPackages() {
      // Depuração: Verifique os dados recebidos
      console.log('Dados recebidos para agrupamento:', this.dnsPackages);

      // Agrupa pacotes DNS por ID
      const groups = this.dnsPackages.reduce((acc, pkg) => {
        if (!pkg.id) return acc; // Ignore pacotes sem ID
        if (!acc[pkg.id]) {
          acc[pkg.id] = {
            id: pkg.id,
            source_ip: pkg.source_ip || 'N/A',
            destination_ip: pkg.destination_ip || 'N/A',
            queries: [],
            answers: []
          };
        }

        // Adiciona queries e answers ao pacote agrupado
        acc[pkg.id].queries = acc[pkg.id].queries.concat(pkg.queries || []);
        acc[pkg.id].answers = acc[pkg.id].answers.concat(pkg.answers || []);

        return acc;
      }, {});

      // Depuração: Verifique o agrupamento dos pacotes
      console.log('Pacotes agrupados por ID:', groups);

      // Converte o objeto de grupos em um array para iteração no template
      return Object.values(groups);
    }
  }
};
</script>

<style scoped>
.dns-packages-table {
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
