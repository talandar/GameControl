<template>
  <div class="container">
    <b-form @submit="getRecap" class="w-100">
      <b-form-group id="form-title-group" label="Raw Text:" label-for="form-raw-input">
        <b-form-textarea
          id="form-raw-input"
          v-model="rawText"
          rows="15"
          required
          placeholder="Enter Recap"
        ></b-form-textarea>
      </b-form-group>
      <b-button type="button" @click="getRecap" variant="primary">Get BBcoded Recap</b-button>
    </b-form>
    <div>{{formattedText}}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Recap',
  components: {
  },
  data() {
    return {
      rawText: '',
      formattedText: 'Submit To Generate',
    };
  },
  methods: {
    getRecap() {
      const path = 'http://192.168.1.111:5000/recap';
      const requestForm = { rawText: this.rawText };
      axios
        .post(path, requestForm)
        .then((res) => {
          this.formattedText = res.data.msg;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {},
};
</script>
