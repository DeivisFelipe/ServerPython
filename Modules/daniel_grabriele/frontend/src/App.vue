<template>
  <dashboard-packages/>
</template>

<script>
import DashboardPackages from './components/DashboardPackages.vue'

export default {
  components: { DashboardPackages },
  name: 'App',

}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
