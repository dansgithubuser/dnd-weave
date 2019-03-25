<template lang='pug'>
div
  h1 Secretmaker
  h3 Name
  input(type='text' v-model='secret.name')
  h3 Coarse
  ol
    li(v-for='i in secret.vue_coarse')
      input(type='text' v-model='i.value', size=65)
  h3 Generation
  input(type='text' v-model='secret.generation', size=65)
  h3 Subproblems
  input(type='text' v-model='secret.subproblems')
  h3 Manage
  input(type='button' value='Save' @click='update')
  input(type='button' value='Delete' @click='del')
  input(type='button' value='New' @click='create')
  h2 Secrets
  ul
    li(v-for='i in secret_ids')
      button(@click='retrieveOne(i.id)') {{ i.name || i.id }}
</template>

<script>
import axios from 'axios'

function get_csrf_token () {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  if (match) return match[1];
}

export default {
  name: 'secretmaker',
  data: function () {
    return {
      secret_ids: [],
      secret: {},
      axios_config: {},
    };
  },
  methods: {
    create: async function () {
      const res = await axios.post('/secret', {}, this.axios_config);
      this.load(res.data);
    },
    retrieve: async function () {
      axios.get('/secret').then((r) => { this.secret_ids = r.data });
    },
    retrieveOne: async function (id) {
      const res = await axios.get(`/secret/${id}`);
      this.load(res.data);
    },
    update: async function () {
      this.secret.coarse = this.secret.vue_coarse.map((i) => i.value);
      await axios.patch(
        `/secret/${this.secret.id}`,
        {
          name: this.secret.name,
          serialized: JSON.stringify(this.secret),
        },
        this.axios_config,
      );
    },
    del: async function () {
      await axios.delete(`/secret/${this.secret.id}`, this.axios_config);
      await this.retrieve();
    },
    load: function (data) {
      const json = JSON.parse(data.serialized);
      this.secret = json;
      this.secret.vue_coarse = this.secret.coarse.map((i) => ({ value: i }));
      this.secret.id = data.id;
      this.secret.name = data.name || this.secret.id;
    },
  },
  mounted: async function () {
    this.retrieve();
    this.axios_config = { headers: { 'X-CSRFToken': get_csrf_token() } }
  }
}
</script>
