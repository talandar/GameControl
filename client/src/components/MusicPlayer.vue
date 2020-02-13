<template>
  <div class="container">
  <center>
    <h2>Music Player</h2>
    <h3><i class="fas fa-stop-circle" v-on:click="stopPlayback()" /></h3>
  </center>
  <b-button class="btn btn-lg btn-success btn-block"
          v-for="list in playlists" v-bind:key="list"
          v-on:click="playPlaylist(list.name)">
            {{list.name}}: {{list.numfiles}} files
  </b-button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MusicPlayer',
  components: {
  },
  mounted() {
    this.getPlaylistData();
  },
  data() {
    return {
      playlists: [],
    };
  },
  methods: {
    getPlaylistData() {
      const path = 'http://192.168.1.111:5000/music/playlistdata';
      axios
        .get(path)
        .then((res) => {
          this.playlists = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    playPlaylist(listName) {
      const path = `http://192.168.1.111:5000/music/play/${listName}`;
      axios.get(path);
    },
    stopPlayback() {
      const path = 'http://192.168.1.111:5000/music/stop';
      axios.get(path);
    },
  },
  created() {},
};
</script>
