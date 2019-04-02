<template lang='pug'>
div
  h2 Ciphertext
  input(type='number' min=1 max=9 v-model.number='ciphertextSize')
  | number of runes
  div(v-for='(v, i) in ciphertextSize')
    input(type='number' min=0 max=255 value=0 v-model.number='ciphertext[i]')
    | {{ runes[i] }}
</template>

<script>
import axios from 'axios'
import helpers from './helpers.js'

export default {
  props: ['secretId'],
  data: () => ({
    ciphertextSize: 1,
    ciphertext: [0],
    runes: [],
  }),
  methods: {
    async getRunes () {
      const res = await axios.get('/ciphertext_to_runes', {
        params: {
          ciphertext: this.ciphertext.join(','),
          secret_id: this.secretId,
        },
      });
      this.runes = res.data;
      this.$emit('runes', this.runes);
    },
  },
  watch: {
    ciphertext () {
      this.getRunes();
      this.$emit('ciphertext', this.ciphertext);
    },
    ciphertextSize () {
      helpers.arrayResize(this.ciphertext, this.ciphertextSize, () => 0);
    },
    secretId () {
      this.getRunes();
    }
  },
  mounted () {
    this.getRunes();
  },
}
</script>
