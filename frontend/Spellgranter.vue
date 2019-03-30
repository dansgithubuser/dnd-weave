<template lang='pug'>
div
  h1 Spellgranter
  template(v-if='spells.length')
    h2 Spells
    ul
      li(v-for='i in spells')
        input(type='button' :value='i.runes' @click='inspectSpell(i)')
  template(v-if='spell')
    Spell(:dict='spell.dict')
    input(type='button' value='grant' @click='grant')
  CharacterSelector(
    :retrieveUrl='"resource/Character/secret_kept"'
    @character='character=$event; get_spells()'
  )
</template>

<script>
import CharacterSelector from './CharacterSelector.vue'
import Spell from './Spell.vue'
import get_csrf_token from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'spellgranter',
  components: {
    CharacterSelector,
    Spell,
  },
  data: function () {
    return {
      character: CharacterSelector.data().character,
      spells: [],
      spell: null,
    };
  },
  methods: {
    get_spells: function () {
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
        level: this.spell.dict.level,
      }, this.axios_config);
    },
  },
  mounted: function () {
    this.axios_config = { headers: { 'X-CSRFToken': get_csrf_token() } }
  }
}
</script>
