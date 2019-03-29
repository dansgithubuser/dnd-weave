<template lang='pug'>
div
  h1 Spellgranter
</template>

<script>
import get_csrf_token from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'spellgranter',
  data: function () {
    return {
    };
  },
  methods: {
  },
  mounted: function () {
    this.axios_config = { headers: { 'X-CSRFToken': get_csrf_token() } }
  }
}
</script>
