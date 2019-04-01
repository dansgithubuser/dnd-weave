<template lang='pug'>
div
  h2 Characters
  ul
    li(v-for='i in characters')
      input(type='button' :value='i.name || i.id' @click='retrieveOne(i.id)')
    li(v-if='allowNew')
      input(type='button' value='New' @click='create')
</template>

<script>
import getCsrfToken from './get_csrf_token.js'

import axios from 'axios'

export default {
  props: {
    retrieveUrl: { default: '/resource/Character' },
    allowNew: { default: true },
  },
  data: () => ({
    characters: [],
    character: {},
  }),
  methods: {
    async create () {
      const res = await axios.post('/resource/Character/', {}, this.axiosConfig);
      this.load(res.data);
      this.retrieve();
    },
    async retrieve () {
      this.characters = (await axios.get(this.retrieveUrl)).data;
    },
    async retrieveOne (id) {
      const res = await axios.get(`/resource/Character/${id}`);
      this.load(res.data);
    },
    async update () {
      await axios.patch(
        `/resource/Character/${this.character.id}/`,
        { name: this.character.name },
        this.axiosConfig,
      );
      this.retrieve();
    },
    load (data) {
      this.character = data;
      this.character.name = this.character.name || this.character.id;
      this.$emit('character', this.character);
    },
  },
  mounted () {
    this.retrieve();
    this.axiosConfig = { headers: { 'X-CSRFToken': getCsrfToken() } }
  },
}
</script>
