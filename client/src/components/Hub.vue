<template>
  <div>
  <b-tabs content-class="mt-3">
    <b-tab title="Music Player" active><MusicPlayer /></b-tab>
    <b-tab title="Lights" disabled><p>I'm a disabled tab!</p></b-tab>
    <b-tab title="Image Control" disabled><p>I'm a disabled tab!</p></b-tab>
    <b-tab title="Npc Generator" disabled><p>I'm a disabled tab!</p></b-tab>
    <b-tab title="Recap"><Recap /></b-tab>
    <b-tab title="Playlist Editor"><PlaylistEditor /></b-tab>
  </b-tabs>
</div>
</template>

<script>
import Recap from './Recap.vue';
import MusicPlayer from './MusicPlayer.vue';
import PlaylistEditor from './PlaylistEditor.vue';

export default {
  name: 'Hub',
  components: {
    Recap,
    MusicPlayer,
    PlaylistEditor,
  },
};
</script>
