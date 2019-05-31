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
    h3 Manage
    input(type='button' value='Save' @click='$refs.characterSelector.update')
    template(v-if='character.secret_id')
      h2 Runes
      input(type='text' v-model='runes' v-on:keyup.enter='research')
      input(type='button' value='Research' @click='research')
    template(v-if='spells.length')
      h2 Spells
      ul
        li(v-for='i in spells')
          input(type='button' :value='i.runes' :disabled='i.dict ? false : true' @click='spell = i')
      input(type='button' value='Refresh' @click='getSpells()')
    template(v-if='spell')
      Spell(:dict='spell.dict')
  CharacterSelector(
    @character='character=$event; getSpells()'
    ref='characterSelector'
  )
</template>

<script>
import PlaintextExplorer from './PlaintextExplorer.vue'
import CharacterSelector from './CharacterSelector.vue'
import Spell from './Spell.vue'
import getCsrfToken from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'character_delver',
  components: {
    PlaintextExplorer,
    CharacterSelector,
    Spell,
  },
  data: () => ({
    character: CharacterSelector.data().character,
    runes: '',
    spells: [],
    spell: null,
  }),
  methods: {
    async accept (offerId) {
      await axios.post('/accept', {
        character_id: this.character.id,
        offer_id: offerId,
      }, this.axiosConfig);
      this.$refs.characterSelector.retrieveOne(this.character.id);
    },
    async research () {
      await axios.post('/research', {
        character_id: this.character.id,
        runes: this.runes,
      }, this.axiosConfig);
      this.runes = '';
      this.getSpells();
    },
    async getSpells () {
      this.spells = (await axios.get('/spells', {
        params: { character_id: this.character.id },
      })).data;
    },
  },
  mounted () {
    this.axiosConfig = { headers: { 'X-CSRFToken': getCsrfToken() } }
    if (initialCharacterId !== null)
      this.$refs.characterSelector.retrieveOne(initialCharacterId);
  },
}
</script>
