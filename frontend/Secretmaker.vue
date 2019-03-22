<template lang='pug'>
div
  h1 Secretmaker
  button(@click='create')
    | c
  button(@click='retrieve')
    | ra
  button(@click='retrieve1')
    | r1
  button(@click='update')
    | u
  button(@click='delet')
    | d
</template>

<script>
import axios from 'axios'

function get_csrf_token () {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  if (match) return match[1];
}

export default {
  name: 'secretmaker',
  data: function () {
    return {
    };
  },
  methods: {
    create: async function () {
      console.log(await axios.post('/secret', {}, { headers: { 'X-CSRFToken': get_csrf_token() } }));
    },
    retrieve: async function () {
      console.log(await axios.get('/secret'));
    },
    retrieve1: async function () {
      console.log(await axios.get('/secret/1'));
    },
    update: async function () {
      console.log(await axios.patch('/secret/1', {
        serialized: 'hello',
      }, { headers: { 'X-CSRFToken': get_csrf_token() } }));
    },
    delet: async function () {
      console.log(await axios.delete('/secret/1', { headers: { 'X-CSRFToken': get_csrf_token() } }));
    },
  },
}
</script>
