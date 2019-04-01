<template lang='pug'>
div
  h2 Ciphertext
  input(type='number' min=1 v-model.number='ciphertextSize')
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
  data: function () {
    return {
      ciphertextSize: 1,
      ciphertext: [0],
      runes: [],
    };
  },
  methods: {
    getRunes: async function () {
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
    ciphertext: function () {
      this.getRunes();
      this.$emit('ciphertext', this.ciphertext);
    },
    ciphertextSize: function () {
      helpers.arrayResize(this.ciphertext, this.ciphertextSize, () => 0);
    },
    secretId: function () {
      this.getRunes();
    }
  },
  mounted: function () {
    this.getRunes();
  },
}
</script>
