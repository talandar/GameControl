<template>
  <div>
  <b-tabs content-class="mt-3">
    <b-tab title="Lights" disabled><p>I'm a disabled tab!</p></b-tab>
    <b-tab title="Image Control" disabled><p>I'm a disabled tab!</p></b-tab>
    <b-tab title="Npc Generator" disabled><p>I'm a disabled tab!</p></b-tab>
    <b-tab title="Recap"><Recap /></b-tab>
  </b-tabs>
</div>
</template>

<script>
import Recap from './Recap.vue';

export default {
  name: 'Hub',
  components: {
    Recap,
  },
};
</script>
