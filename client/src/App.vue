<template>
  <div id="app">
    <Ping msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import Ping from './components/Ping.vue';

export default {
  name: 'app',
  components: {
    Ping,
  },
};
</script>

<style>
#app {
  margin-top: 60px;
}
</style>
