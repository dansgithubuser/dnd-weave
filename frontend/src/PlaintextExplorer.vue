<template lang='pug'>
div
  form(@submit.prevent='submit')
    input(
      type='text'
      size=80
      v-model='plaintext'
    )
    input(type='submit')
    input(type='button' value='Random' @click='random')
  textarea(rows=20 cols=80 v-model='english')
</template>

<script>
export default {
  name: 'plaintext_explorer',
  data: function () {
    return {
      english: '',
      plaintext: '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
    };
  },
  methods: {
    async submit () {
      const url = `${window.location.protocol}//${window.location.host}/plaintext_to_dict?plaintext=${this.plaintext}`;
      const response = await fetch(url);
      const j = await response.json();
      this.english = Object.entries(j).map(function(i) {
        if (i[0] === 'extra') return i[1].join('\n');
        return `${i[0]}: ${i[1]}`;
      }).join('\n');
    },
    async random () {
      this.plaintext = Array.from({ length: 16 }, i => Math.floor(Math.random() * 256)).join(' ');
      await this.submit();
    },
  },
}
</script>
