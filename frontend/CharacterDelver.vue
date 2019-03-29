<template lang='pug'>
div
  h1 Character Delver
</template>

<script>
import PlaintextExplorer from './PlaintextExplorer.vue'
import get_csrf_token from './get_csrf_token.js'

import axios from 'axios'

export default {
  name: 'character_delver',
  components: {
    PlaintextExplorer,
  },
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
