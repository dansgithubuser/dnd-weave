<template lang='pug'>
div
  h1 plaintext explorer
  h2 controls
  form(@submit.prevent='submit')
    input(
      type='text'
      size=65
      v-model='plaintext'
      @input='submit("plaintext")'
    )
    input(type='button' value='Random' @click='random')
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
          v-model=`features[${i}]`
          @input=`submit(${i})`
        )
        = v
  h2 spell
  ul(v-html='english')
  h2 extra (elemental)
  ul(v-html='extra')
  h2 extra (generic)
  ul(v-html='misc')
</template>

<script>
import axios from 'axios'

export default {
  name: 'plaintext_explorer',
  data: function () {
    return {
      english: '',
      plaintext: '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0',
      features: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      extra: '',
      misc: '',
    };
  },
  methods: {
    async submit (feature) {
      if (feature != 'plaintext') {
        this.plaintext = this.features.join(' ');
      } else {
        this.plaintext.split(' ').forEach((v, i) => {
          this.features[i] = v;
        });
      }
      const response = await axios.get(`/plaintext_to_dict?plaintext=${this.plaintext}`);
      this.english = Object.entries(response.data).map((i) => {
        var style = '';
        if (i[0] === 'element') {
          const [color, shadowColor] = {
            'force': ['lightgrey', 'purple'],
            'antiforce': ['lightgrey', 'purple'],
            'fire': ['red', 'red'],
            'cold': ['blue', 'blue'],
            'lightning': ['lightblue', 'black'],
            'antilightning': ['lightblue', 'black'],
            'light': ['yellow', 'black'],
            'dark': ['black', 'yellow'],
            'thunder': ['grey', 'grey'],
            'antithunder': ['grey', 'grey'],
            'healing': ['#00ff00', 'black'],
            'necrotic': ['#000000', 'black'],
            'acid': ['#888000', '#888000'],
            'poison': ['purple', 'purple'],
            'psychic': ['pink', 'black'],
            'radiant': ['orange', 'black'],
            'wind': ['white', 'blue'],
            'water': ['cyan', 'blue'],
            'earth': ['brown', 'brown'],
          }[i[1]] || 'lightgrey';
          style = `color:${color}; font-weight:bold; text-shadow: 0px 0px 2px ${shadowColor}`;
        }
        var a;
        if (i[0] === 'extra') a = i[1];
        else a = [`${i[0]}: <span style='${style}'>${i[1]}</b>`];
        return a.map((i) => `<li>${i}</li>`).join('');
      }).join('');
      axios.get(`/extras?element=${response.data['element']}`).then((r) => 
        this.extra = r.data.map((v, i) =>
          `<li>${i * 4}: ${v[0]}</li>`
        ).join('')
      );
    },
    async random () {
      this.plaintext = Array.from({ length: 16 }, i => Math.floor(Math.random() * 256)).join(' ');
      await this.submit('plaintext');
    },
  },
  mounted: async function () {
    this.submit();
    axios.get('/extras').then((r) =>
      this.misc = r.data.map((v, i) =>
        `<li>${Math.floor(i * 4 / 3) + 1}: ${v[0]}</li>`
      ).join('')
    );
  },
}
</script>
