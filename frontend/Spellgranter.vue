<template lang='pug'>
div
  h1 Spellgranter
  template(v-if='spells.length')
    h2 Spells
    ul
      li(v-for='i in spells')
        input(type='button' :value='i.runes' @click='inspectSpell(i)')
  template(v-if='character.secret_id')
    Runes(
      :secret_id='character.secret_id'
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
    :retrieveUrl='"resource/Character/secret_kept"'
    :allowNew='false'
    @character='character=$event; getSpells()'
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
    getSpells: function () {
      axios.get('/spells', {
        params: { character_id: this.character.id },
      }).then(r => this.spells = r.data);
    },
    inspectSpell: function (spell) {
      this.spell = spell;
      if (!this.spell.dict) {
        axios.get('/grant', { params: { spell_id: this.spell.id } })
          .then(r => this.spell.dict = r.data);
      }
    },
    grant: function () {
      axios.post('/grant', {
        spell_id: this.spell.id,
        character_id: this.character.id,
        runes: this.runes.join(' '),
        level: this.spell.dict.level,
      }, this.axiosConfig).then(() => this.getSpells());
    },
  },
  watch: {
    runes: async function () {
      axios.get('/runes_to_dict', {
        params: {
          runes: this.runes.join(' '),
          secret_id: this.character.secret_id,
        },
      }).then(r => { this.spell = { dict: r.data } });
    },
  },
  mounted: function () {
    this.axiosConfig = { headers: { 'X-CSRFToken': getCsrfToken() } }
  }
}
</script>
