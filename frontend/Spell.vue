<template lang='pug'>
div
  h2 Spell
  ul(v-html='english')
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
  },
  data: function () {
    return {
      english: '',
      extra: '',
    };
  },
  methods: {
    async submit () {
      const response = await axios.get('/plaintext_to_dict', {
        params: { plaintext: this.plaintext.join(',') },
      });
      this.load(response.data);
    },
    async load (data) {
      this.english = Object.entries(data).map(i => {
        //spell feature styling
        var style = '';
        if (i[0] === 'element') {
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
          }[i[1]] || 'lightgrey';
          style = `
            color: ${colors[0]};
            font-weight: bold;
            text-shadow: 1px 1px 3px ${colors[1]};
            letter-spacing: 1px;
            text-transform: uppercase;
            background-image: linear-gradient(to bottom right, ${colors[2]}, ${colors[3]});
          `;
        }
        else if (i[0] === 'range' && i[1] === 'infinity'
          || i[0] === 'shape' && i[1].startsWith('inf')
        ) style = 'text-transform: uppercase; font-weight: bold;';
        else if (i[0] === 'duration') {
          if (i[1].includes('hours')) style = 'text-transform: uppercase;';
          else if (i[1].includes('days')) style = 'text-transform: uppercase; font-weight: bold;';
        }
        //spell feature formatting
        var a;
        if (i[0] === 'extra') a = i[1];
        else a = [`${i[0]}: <span style='${style}'>&nbsp; ${i[1]} &nbsp;</span>`];
        return a.map(i => `<li>${i}</li>`).join('');
      }).join('');
      axios.get(`/plaintext_extras?element=${data['element']}`).then(r =>
        this.$emit('extra', this.extra = r.data.map((v, i) =>
          `<li>${i * 4}: ${v[0]}</li>`
        ).join(''))
      );
    },
  },
  watch: {
    plaintext: async function () {
      this.submit();
    },
    dict: function () {
      this.load(this.dict);
    },
  },
  mounted: function () {
    if (this.dict.element) this.load(this.dict);
    else this.submit();
  },
}
</script>
