<template lang='pug'>
div
  h1 Plaintext explorer
  h2 Plaintext
  div
    | {{ plaintext.join(',') }}
  div
    - const features = [
    -   'element',
    -   'damage dice shape',
    -   'damage dice number',
    -   'range',
    -   'shape',
    -   'shape size',
    -   'targets, number of extras',
    -   'concentration',
    -   'duration',
    -   'long duration',
    -   'casting time',
    -   'long casting time',
    -   'delivery',
    -   'extra 1',
    -   'extra 2',
    -   'extra 3',
    - ];
    each v, i in features
      div
        input(
          type='number'
          min=0
          max=256
          v-model.number=`plaintext[${i}]`
        )
        = v
  input(type='button' value='Random' @click='random')
  Spell(
    :plaintext='plaintext'
    @extra='extra=$event'
  )
  h2 Extra (elemental)
  ul(v-html='extra')
  h2 Extra (generic)
  ul(v-html='misc')
</template>

<script>
import Spell from './Spell.vue'

import axios from 'axios'

export default {
  name: 'plaintext_explorer',
  components: {
    Spell,
  },
  data: () => ({
    plaintext: Spell.props.plaintext.default(),
    extra: '',
    misc: '',
  }),
  methods: {
    random () {
      this.plaintext = Array.from({ length: 16 }, i => Math.floor(Math.random() * 256));
    },
  },
  async mounted () {
    this.misc = (await axios.get('/plaintext_extras')).data.map(
      (v, i) => `<li>${Math.floor(i * 4 / 3) + 1}: ${v[0]}</li>`,
    ).join('');
  },
}
</script>
