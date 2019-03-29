<template lang='pug'>
div
  h1 Secretmaker
  template(v-if='secret.id')
    h3 Name
    input(type='text' v-model='secret.name')
    h3 Coarse
    ol
      li(v-for='i in secret.vue_coarse')
        input(type='text' v-model='i.value' size=65)
    h3 Generation
    input(type='text' v-model='secret.generation' size=65)
    h3 Subproblems
    input(type='text' v-model='secret.subproblems')
    h3 Manage
    div
      input(type='button' value='Save' @click='update')
    div
      input(type='text' placeholder='player' v-model='player')
      input(type='text' placeholder='character' v-model='character')
      input(type='button' value='Offer' @click='offer' v-bind:style='offerStyle')
    Runes(
      :secret='secret'
      @ciphertext='ciphertext=$event'
    )
    Spell(:plaintext='plaintext')
  h2 Secrets
  ul
    li(v-for='i in secrets')
      input(type='button' :value='i.name || i.id' @click='retrieveOne(i.id)')
    li
      input(type='button' value='New' @click='create')
</template>

<script>
import Runes from './Runes.vue'
import Spell from './Spell.vue'
import get_csrf_token from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'secretmaker',
  components: {
    Runes,
    Spell,
  },
  data: function () {
    return {
      secrets: [],
      secret: {},
      axios_config: {},
      ciphertext: Runes.data().ciphertext,
      player: '',
      character: '',
      offerStyle: '',
      plaintext: Spell.props.plaintext.default,
    };
  },
  methods: {
    create: async function () {
      const res = await axios.post('/resource/Secret/', {}, this.axios_config);
      this.load(res.data);
      this.retrieve();
    },
    retrieve: function () {
      axios.get('/resource/Secret').then(r => { this.secrets = r.data });
    },
    retrieveOne: async function (id) {
      const res = await axios.get(`/resource/Secret/${id}`);
      this.load(res.data);
    },
    update: async function () {
      this.secret.coarse = this.secret.vue_coarse.map(i => i.value);
      await axios.patch(
        `/resource/Secret/${this.secret.id}/`,
        {
          name: this.secret.name,
          serialized: JSON.stringify(this.secret),
        },
        this.axios_config,
      );
      this.retrieve();
    },
    load: function (data) {
      const json = JSON.parse(data.serialized);
      this.secret = json;
      this.secret.vue_coarse = this.secret.coarse.map(i => ({ value: i }));
      this.secret.id = data.id;
      this.secret.name = data.name || this.secret.id;
      this.get_plaintext();
    },
    get_plaintext: async function () {
      const res = await axios.get('/ciphertext_to_plaintext', {
        params: {
          ciphertext: this.ciphertext.join(','),
          secret_id: this.secret.id,
        },
      });
      this.plaintext = res.data;
    },
    offer: function () {
      axios.post('/offer', {
        secret_id: this.secret.id,
        player: this.player,
        character_name: this.character,
      }, this.axios_config)
        .then(() => { this.offerStyle = ''; })
        .catch(() => { this.offerStyle = 'background-color:red'; });
    },
  },
  watch: {
    ciphertext: function () {
      this.get_plaintext();
    },
  },
  mounted: function () {
    this.retrieve();
    this.axios_config = { headers: { 'X-CSRFToken': get_csrf_token() } }
  }
}
</script>
