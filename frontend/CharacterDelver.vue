<template lang='pug'>
div
  h1 Character Delver
  template(v-if='character.id')
    h3 Name
    input(type='text' v-model='character.name')
    template(v-if='character.offers.length && !character.secret_id')
      h3 Accept
      ul
        li(v-for='i in character.offers')
          input(type='button' :value='i.secret.name || i.secret.id' @click='accept(i.id)')
    template(v-if='character.secret_id')
      h2 Runes
      input(type='text' v-model='runes')
      input(type='button' value='Research' @click='research')
    template(v-if='spells.length')
      h2 Spells
      ul
        li(v-for='i in spells')
          input(type='button' :value='i.runes' disabled='i.dict ? false : true')
  h2 Characters
  ul
    li(v-for='i in characters')
      input(type='button' :value='i.name || i.id' @click='retrieveOne(i.id)')
    li
      input(type='button' value='New' @click='create')
</template>

<script>
import PlaintextExplorer from './PlaintextExplorer.vue'
import get_csrf_token from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'character_delver',
  components: {
    PlaintextExplorer,
  },
  data: function () {
    return {
      characters: [],
      character: {},
      runes: '',
      spells: [],
    };
  },
  methods: {
    create: async function () {
      const res = await axios.post('/resource/Character/', {}, this.axios_config);
      this.load(res.data);
      this.retrieve();
    },
    retrieve: function () {
      axios.get('/resource/Character').then(r => { this.characters = r.data });
    },
    retrieveOne: async function (id) {
      const res = await axios.get(`/resource/Character/${id}`);
      this.load(res.data);
      this.get_spells();
    },
    load: function (data) {
      this.character = data;
      this.character.name = this.character.name || this.character.id;
    },
    accept: function (offer_id) {
      axios.post('/accept', {
        character_id: this.character.id,
        offer_id,
      }, this.axios_config);
    },
    research: function () {
      axios.post('/research', {
        character_id: this.character.id,
        runes: this.runes,
      }, this.axios_config).then(() => this.get_spells());
    },
    get_spells: function () {
      axios.get('/spells', {
        params: { character_id: this.character.id },
      }).then(r => this.spells = r.data);
    },
  },
  mounted: function () {
    this.retrieve();
    this.axios_config = { headers: { 'X-CSRFToken': get_csrf_token() } }
  }
}
</script>
