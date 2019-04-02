<template lang='pug'>
div
  h1 Spellgranter
  template(v-if='character.name')
    h3 Character
    | {{ character.name }}
  template(v-if='spells.length')
    h2 Spells
    ul
      li(v-for='i in spells')
        input(type='button' :value='i.runes' @click='inspectSpell(i)')
  template(v-if='character.secret_id')
    Runes(
      :secretId='character.secret_id'
      @runes='runes=$event'
    )
  template(v-if='spell')
    Spell(
      :dict='spell.dict'
      :editableLevel='true'
      @level='spell.dict.level=$event'
    )
    input(type='button' value='grant' @click='grant')
  CharacterSelector(
    :retrieveUrl='"/resource/Character/spellgrantees"'
    :allowNew='false'
    @character='character=$event; getSpells()'
    ref='characterSelector'
  )
</template>

<script>
import CharacterSelector from './CharacterSelector.vue'
import Spell from './Spell.vue'
import Runes from './Runes.vue'
import getCsrfToken from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'spellgranter',
  components: {
    CharacterSelector,
    Spell,
    Runes,
  },
  data: function () {
    return {
      character: CharacterSelector.data().character,
      spells: [],
      spell: null,
      runes: [],
    };
  },
  methods: {
    async getSpells () {
      this.spells = (await axios.get('/spells', {
        params: { character_id: this.character.id },
      })).data;
    },
    async inspectSpell (spell) {
      this.spell = spell;
      if (!this.spell.dict)
        this.spell.dict = (await axios.get('/grant', { params: {
          spell_id: this.spell.id,
        } })).data;
    },
    async grant () {
      await axios.post('/grant', {
        spell_id: this.spell.id,
        character_id: this.character.id,
        runes: this.runes.join(' '),
        level: this.spell.dict.level,
      }, this.axiosConfig);
      this.getSpells();
    },
  },
  watch: {
    async runes () {
      this.spell = { dict: (await axios.get('/runes_to_dict', {
        params: {
          runes: this.runes.join(' '),
          secret_id: this.character.secret_id,
        },
      })).data };
    },
  },
  mounted () {
    this.axiosConfig = { headers: { 'X-CSRFToken': getCsrfToken() } }
    if (initialCharacterId !== null)
      this.$refs.characterSelector.retrieveOne(initialCharacterId);
  },
}
</script>
