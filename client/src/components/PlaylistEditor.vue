<template>
  <div class="wide">
  <center>
    <h2>Playlist Editor</h2>
    <br />
    <h3>
      <i class="fas fa-sync" v-on:click="getFileData()" />
      <i class="fas fa-stop-circle" v-on:click="stopPlayback()" />
    </h3>
  </center>
  <br />
  New Playlist:
  <input v-model="newList" placeholder="new">&nbsp;
  <i class="fas fa-plus-circle" v-on:click="newPlaylist()" />
  <br /><br />
  <b-table-simple hover large caption-top responsive>
    <colgroup><col><col></colgroup>
    <colgroup><col v-for="list in playlists" v-bind:key="list"></colgroup>
    <b-thead head-variant="dark">
      <b-tr>
        <b-th>Play</b-th>
        <b-th>Filename</b-th>
        <b-th v-for="playlist in playlists" v-bind:key="playlist">
          {{playlist}} <i class="fas fa-minus-circle" v-on:click="removePlaylist(playlist)" />
        </b-th>
      </b-tr>
    </b-thead>
    <b-tbody>
      <b-tr v-for="(lists, file) in files" v-bind:key="file">
        <b-td><i class="fas fa-play-circle" v-on:click="playFile(file)"></i></b-td>
        <b-td>{{file.substring(root.length)}}</b-td>
        <b-td v-for="(value, listname) in lists" v-bind:key="listname">
          <b-button
          v-bind:class="['btn', 'btn-sm', value ? 'btn-success' : 'btn-danger' ]"
          v-on:click="toggleListInclusion(file,listname,value)">
            {{listname}}
          </b-button>
        </b-td>
      </b-tr>
    </b-tbody>
  </b-table-simple>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PlaylistEditor',
  components: {
  },
  mounted() {
    this.getFileData();
  },
  data() {
    return {
      playlists: [],
      files: {},
      root: '',
      newList: '',
    };
  },
  methods: {
    getFileData() {
      const path = 'http://192.168.1.111:5000/music/filedata';
      axios
        .get(path)
        .then((res) => {
          this.playlists = res.data.lists;
          this.files = res.data.files;
          this.root = res.data.root;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    playFile(file) {
      const path = 'http://192.168.1.111:5000/music/playfile';
      const arg = { file };
      axios.post(path, arg);
    },
    stopPlayback() {
      const path = 'http://192.168.1.111:5000/music/stop';
      axios.get(path);
    },
    newPlaylist() {
      const path = `http://192.168.1.111:5000/music/playlist/${this.newList}`;
      axios.put(path);
      this.getFileData();
      this.newList = '';
    },
    removePlaylist(listname) {
      const path = `http://192.168.1.111:5000/music/playlist/${listname}`;
      axios.delete(path);
      this.getFileData();
    },
    toggleListInclusion(file, listname, oldValue) {
      const path = 'http://192.168.1.111:5000/music/file';
      const arg = { file, list: listname };
      if (oldValue) { // currently in, remove from list
        axios.delete(path, { data: { arg } });
      } else { // currently not in, adding
        axios.put(path, arg);
      }
      this.getFileData();
    },
  },
  created() {},
};
</script>
