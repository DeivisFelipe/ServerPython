<template>
  <div>
    <label for="fileInput" class="float-button upload-button">Selecionar Arquivo</label>
    <input id="fileInput" ref="fileInput" type="file" style="display: none" @change="uploadArquivo">
    <h1>Listagem de pacotes</h1>
    <ul>
      <li v-for="pacote in pacotes" :key="pacote.timestamp">
        <p>Timestamp: {{ pacote.timestamp }}</p>
        <p>MAC de Origem: {{ pacote.mac_origem }}</p>
        <p>MAC de Destino: {{ pacote.mac_destino }}</p>
        <p>IP de Origem: {{ pacote.ip_origem }}</p>
        <p>IP de Destino: {{ pacote.ip_destino }}</p>
        <p>Protocolo: {{ pacote.protocolo }}</p>
        <p>Tipo de Ethernet: {{ pacote.tipo_ethernet }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'ListPackages',
  data() {
    return {
      pacotes: []
    };
  },
  methods: {
    async uploadArquivo(event) {
      const arquivo = event.target.files[0];
      const formData = new FormData();
      formData.append("arquivo_pcap", arquivo);

      try {
        const response = await axios.post("http://localhost:8000/listar_pacotes", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });

        // Atualiza os pacotes com os dados recebidos
        this.pacotes = response.data.pacotes;
      } catch (error) {
        console.error("Erro ao enviar arquivo:", error);
      }
    }
  }
};
</script>

<style scoped>
.float-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}

.btn-floating {
  background-color: #232343;
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0px 0px 5px rgba(112, 106, 106, 0.5);
}

.upload-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #232343;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 15px 25px;
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0px 0px 5px rgba(112, 106, 106, 0.5);
}
</style>
