<template lang='pug'>
div
  h1 Spellgranter
  template(v-if='spells.length')
    h2 Spells
    ul
      li(v-for='i in spells')
        input(type='button' :value='i.runes')
  CharacterSelector(
    :retrieveUrl='"resource/Character/secret_kept"'
    @character='character=$event; get_spells()'
  )
</template>

<script>
import CharacterSelector from './CharacterSelector.vue'
import get_csrf_token from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'spellgranter',
  components: {
    CharacterSelector,
  },
  data: function () {
    return {
      character: CharacterSelector.data().character,
      spells: [],
    };
  },
  methods: {
    get_spells: function () {
      axios.get('/spells', {
        params: { character_id: this.character.id },
      }).then(r => this.spells = r.data);
    },
  },
  mounted: function () {
    this.axios_config = { headers: { 'X-CSRFToken': get_csrf_token() } }
  }
}
</script>
