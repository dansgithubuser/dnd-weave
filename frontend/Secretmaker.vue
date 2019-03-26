<template lang='pug'>
div
  h1 Secretmaker
  template(v-if='this.secret.id')
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
    h2 Controls
    input(type='number' min=1 v-model.number='ciphertext_size')
    | number of runes
    div(v-for='(v, i) in ciphertext_size')
      input(type='number' min=0 max=255 value=0 v-model.number='ciphertext[i]')
      | {{ runes[i] }}
    PlaintextExplorer(
      ref='plaintext_explorer'
      :hidden="['title', 'controls', 'extra']"
    )
  h2 Secrets
  ul
    li(v-for='i in secret_ids')
      button(@click='retrieveOne(i.id)') {{ i.name || i.id }}
</template>

<script>
import PlaintextExplorer from './PlaintextExplorer.vue'
import get_csrf_token from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'secretmaker',
  components: {
    PlaintextExplorer,
  },
  data: function () {
    return {
      secret_ids: [],
      secret: {},
      axios_config: {},
      ciphertext_size: 1,
      ciphertext: [0],
      runes: [],
    };
  },
  methods: {
    create: async function () {
      const res = await axios.post('/secret', {}, this.axios_config);
      this.load(res.data);
      this.retrieve();
    },
    retrieve: function () {
      axios.get('/secret').then(r => { this.secret_ids = r.data });
    },
    retrieveOne: async function (id) {
      const res = await axios.get(`/secret/${id}`);
      this.load(res.data);
    },
    update: async function () {
      this.secret.coarse = this.secret.vue_coarse.map(i => i.value);
      await axios.patch(
        `/secret/${this.secret.id}`,
        {
          name: this.secret.name,
          serialized: JSON.stringify(this.secret),
        },
        this.axios_config,
      );
      this.retrieve();
    },
    del: async function () {
      await axios.delete(`/secret/${this.secret.id}`, this.axios_config);
      this.retrieve();
    },
    load: function (data) {
      const json = JSON.parse(data.serialized);
      this.secret = json;
      this.secret.vue_coarse = this.secret.coarse.map(i => ({ value: i }));
      this.secret.id = data.id;
      this.secret.name = data.name || this.secret.id;
      this.get_runes();
      this.get_plaintext();
    },
    get_runes: async function () {
      const res = await axios.get('/ciphertext_to_runes', {
        params: {
          ciphertext: this.ciphertext.join(','),
          secret_id: this.secret.id,
        },
      });
      this.runes = res.data;
    },
    get_plaintext: async function () {
      const res = await axios.get('/ciphertext_to_plaintext', {
        params: {
          ciphertext: this.ciphertext.join(','),
          secret_id: this.secret.id,
        },
      });
      this.$refs.plaintext_explorer.plaintext = res.data;
    },
  },
  watch: {
    ciphertext: function () {
      this.get_runes();
      this.get_plaintext();
    },
    ciphertext_size: function () {
      this.ciphertext = this.ciphertext.slice(0, this.ciphertext_size);
      this.ciphertext = this.ciphertext.concat(Array.from(
        { length: this.ciphertext_size - this.ciphertext.length },
        () => 0,
      ));
    },
  },
  mounted: function () {
    this.retrieve();
    this.axios_config = { headers: { 'X-CSRFToken': get_csrf_token() } }
  }
}
</script>
