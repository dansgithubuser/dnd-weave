<template lang='pug'>
div
  h2 Spell
  ul
    li(v-for='v, i in ddict')
      template(v-if='i.startsWith("extra")')
        | {{ v }}
      template(v-else)
        | {{ i }}: 
        span(:style='getStyle(i, v)')
          template(v-if='editableLevel && i == "level"')
            input(type='number' min=0 v-model='ddict.level')
          template(v-else)
            | {{ v }}
</template>

<script>
import axios from 'axios'

export default {
  props: {
    plaintext: {
      default: () => Array.from({length: 16}, i => 0),
    },
    dict: {
      default: () => {},
    },
    editableLevel: {
      default: false,
    },
  },
  data: () => ({
    ddict: {},
    extra: '',
  }),
  methods: {
    async submit () {
      const response = await axios.get('/plaintext_to_dict', {
        params: { plaintext: this.plaintext.join(',') },
      });
      this.load(response.data);
    },
    async load (data) {
      const dict = {};
      for (const i in data) {
        if (i === 'extra') {
          for (const j in data[i]) dict[`extra${j}`] = data[i][j];
        } else {
          dict[i] = data[i];
        }
      }
      this.ddict = dict;
      axios.get(`/plaintext_extras?element=${data['element']}`).then(r =>
        this.$emit('extra', this.extra = r.data.map((v, i) =>
          `<li>${i * 4}: ${v[0]}</li>`
        ).join(''))
      );
    },
    getStyle (feature, value) {
      var style = '';
      if (feature  === 'element') {
        const colors = {
          'force': ['lightblue', 'purple', 'black', 'white'],
          'antiforce': ['lightblue', 'purple', 'white', 'black'],
          'fire': ['orange', 'red', 'black', 'white'],
          'cold': ['#8080ff', 'blue', 'white', 'black'],
          'lightning': ['lightblue', 'black', 'black', 'white'],
          'antilightning': ['lightblue', 'black', 'white', 'black'],
          'light': ['yellow', 'black', 'black', 'white'],
          'dark': ['black', 'yellow', 'white', 'black'],
          'thunder': ['white', 'black', 'black', 'white'],
          'antithunder': ['white', 'black', 'white', 'black'],
          'healing': ['#00ff00', 'black', 'black', 'white'],
          'necrotic': ['black', 'darkred', 'white', 'black'],
          'acid': ['#ccc000', '#202000', '#202000', 'white'],
          'poison': ['#cc00cc', '#200020', '#200020', 'white'],
          'psychic': ['pink', 'black', 'black', 'white'],
          'radiant': ['orange', 'black', 'black', 'white'],
          'wind': ['white', 'blue', 'blue', 'white'],
          'water': ['cyan', 'blue', 'blue', 'white'],
          'earth': ['#00ff00', '#402000', '#402000', 'white'],
        }[value] || 'lightgrey';
        style = `
          color: ${colors[0]};
          font-weight: bold;
          text-shadow: 1px 1px 3px ${colors[1]};
          letter-spacing: 1px;
          text-transform: uppercase;
          background-image: linear-gradient(to bottom right, ${colors[2]}, ${colors[3]});
          padding-left: 1em;
          padding-right: 1em;
        `;
      }
      else if (feature  === 'range' && value === 'infinity'
        || feature === 'shape' && value.startsWith('inf')
      ) style = 'text-transform: uppercase; font-weight: bold;';
      else if (feature === 'duration') {
        if (value.includes('hours')) style = 'text-transform: uppercase;';
        else if (value.includes('days')) style = 'text-transform: uppercase; font-weight: bold;';
      }
      return style;
    },
  },
  watch: {
    async plaintext () {
      this.submit();
    },
    dict () {
      if (!this.dict) return;
      this.load(this.dict);
    },
    'ddict.level' () {
      this.$emit('level', this.ddict.level);
    },
  },
  mounted: function () {
    if (this.dict && this.dict.element) this.load(this.dict);
    else this.submit();
  },
}
</script>
