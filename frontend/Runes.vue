<template lang='pug'>
div
  h2 Ciphertext
  input(type='number' min=1 v-model.number='ciphertext_size')
  | number of runes
  div(v-for='(v, i) in ciphertext_size')
    input(type='number' min=0 max=255 value=0 v-model.number='ciphertext[i]')
    | {{ runes[i] }}
</template>

<script>
import axios from 'axios'

export default {
  props: ['secret'],
  data: function () {
    return {
      ciphertext_size: 1,
      ciphertext: [0],
      runes: [],
    };
  },
  methods: {
    get_runes: async function () {
      const res = await axios.get('/ciphertext_to_runes', {
        params: {
          ciphertext: this.ciphertext.join(','),
          secret_id: this.secret.id,
        },
      });
      this.runes = res.data;
    },
  },
  watch: {
    ciphertext: function () {
      this.get_runes();
      this.$emit('ciphertext', this.ciphertext);
    },
    ciphertext_size: function () {
      this.ciphertext = this.ciphertext.slice(0, this.ciphertext_size);
      this.ciphertext = this.ciphertext.concat(Array.from(
        { length: this.ciphertext_size - this.ciphertext.length },
        () => 0,
      ));
    },
    secret: function () {
      this.get_runes();
    }
  },
}
</script>
