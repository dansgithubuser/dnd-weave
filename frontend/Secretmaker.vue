<template lang='pug'>
div
  h1 Secretmaker
  template(v-if='secret.id')
    h3 Name
    input(type='text' v-model='secret.name')
    h3 Coarse
      span.tooltip ?
        .tooltiptext The first rune of a spell selects a slot. 
          | A slot corresponds to a plaintext, which can be figured with the plaintext explorer. 
          | This is where you can theme what spells a character can typically perform.
    input(type='number' min=1 v-model.number='coarseSize')
    | slots
    div(v-for='i in secret.vueCoarse')
      input(type='text' v-model='i.value' size=65)
    h3 Generation
      span.tooltip ?
        .tooltiptext Slots are organized into generations. 
          | The slots explicitly specified are the first generation. 
          | Latter generations have this value added to them.
    input(type='text' v-model='secret.vueGeneration' size=65)
    h3 Subproblems
      span.tooltip ?
        .tooltiptext Latter runes obey complicated behavior, 
          | modifying the slot specified by the first. 
          | This is where you can theme how a character problem solves with the weave. 
          | Subproblem themes and modification types are:
          | <br>0 - linear, precise
          | <br>1 - spherical, chaotic
          | <br>2 - fractal, medium
    input(type='text' v-model='secret.vueSubproblems')
    h3 Manage
    div
      input(type='button' value='Save' @click='update')
    div
      input(type='text' placeholder='player' v-model='player')
      input(type='text' placeholder='character' v-model='character')
      input(type='button' value='Offer' @click='offer' v-bind:style='offerStyle')
    Runes(
      :secretId='secret.id'
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
import getCsrfToken from './get_csrf_token.js'
import helpers from './helpers.js'

import axios from 'axios'

export default {
  name: 'secretmaker',
  components: {
    Runes,
    Spell,
  },
  data: () => ({
    secrets: [],
    secret: {},
    axiosConfig: {},
    ciphertext: Runes.data().ciphertext,
    player: '',
    character: '',
    offerStyle: '',
    plaintext: Spell.props.plaintext.default(),
    coarseSize: 1,
  }),
  methods: {
    async create () {
      const res = await axios.post('/resource/Secret/', {}, this.axiosConfig);
      this.load(res.data);
      this.retrieve();
    },
    async retrieve () {
      this.secrets = (await axios.get('/resource/Secret')).data;
    },
    async retrieveOne (id) {
      const res = await axios.get(`/resource/Secret/${id}`);
      this.load(res.data);
    },
    async update () {
      this.secret.coarse = this.secret.vueCoarse.map(i => i.value.split(',').map(i => parseInt(i)));
      this.secret.generation = this.secret.vueGeneration.split(',').map(i => parseInt(i));
      this.secret.subproblems = this.secret.vueSubproblems.split(',').map(i => parseInt(i));
      await axios.patch(
        `/resource/Secret/${this.secret.id}/`,
        {
          name: this.secret.name,
          serialized: JSON.stringify(this.secret),
        },
        this.axiosConfig,
      );
      this.retrieve();
    },
    load (data) {
      const json = JSON.parse(data.serialized);
      this.secret = json;
      this.secret.vueCoarse = this.secret.coarse.map(i => ({ value: i.join(',') }));
      this.secret.vueGeneration = this.secret.generation.join(',');
      this.secret.vueSubproblems = this.secret.subproblems.join(',');
      this.secret.id = data.id;
      this.secret.name = data.name || this.secret.id;
      this.coarseSize = this.secret.coarse.length;
      this.getPlaintext();
    },
    async getPlaintext () {
      const res = await axios.get('/ciphertext_to_plaintext', {
        params: {
          ciphertext: this.ciphertext.join(','),
          secret_id: this.secret.id,
        },
      });
      this.plaintext = res.data;
    },
    offer () {
      axios.post('/offer', {
        secret_id: this.secret.id,
        player: this.player,
        character_name: this.character,
      }, this.axiosConfig)
        .then(() => this.offerStyle = '')
        .catch(() => this.offerStyle = 'background-color:red');
    },
  },
  watch: {
    ciphertext () {
      this.getPlaintext();
    },
    coarseSize () {
      helpers.arrayResize(this.secret.vueCoarse, this.coarseSize,
        () => ({ value: Spell.props.plaintext.default().join(',') }));
    },
  },
  mounted () {
    this.retrieve();
    this.axiosConfig = { headers: { 'X-CSRFToken': getCsrfToken() } }
  },
}
</script>
