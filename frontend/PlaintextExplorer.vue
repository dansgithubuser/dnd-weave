<template lang='pug'>
div
  h1 Plaintext explorer
  h2 Controls
  form(@submit.prevent='submit')
    input(
      type='text'
      size=65
      v-model='plaintext'
      @input='submit'
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
          v-model=`plaintext[${i}]`
          @input=`submit`
        )
        = v
  h2 Spell
  ul(v-html='english')
  h2 Extra (elemental)
  ul(v-html='extra')
  h2 Extra (generic)
  ul(v-html='misc')
</template>

<script>
import axios from 'axios'

export default {
  name: 'plaintext_explorer',
  data: function () {
    return {
      english: '',
      plaintext: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      extra: '',
      misc: '',
    };
  },
  methods: {
    async submit () {
      const response = await axios.get(`/plaintext_to_dict?plaintext=${this.plaintext}`);
      this.english = Object.entries(response.data).map((i) => {
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
        return a.map((i) => `<li>${i}</li>`).join('');
      }).join('');
      axios.get(`/plaintext_extras?element=${response.data['element']}`).then((r) =>
        this.extra = r.data.map((v, i) =>
          `<li>${i * 4}: ${v[0]}</li>`
        ).join('')
      );
    },
    async random () {
      this.plaintext = Array.from({ length: 16 }, i => Math.floor(Math.random() * 256));
      await this.submit('plaintext');
    },
  },
  mounted: async function () {
    this.submit();
    axios.get('/plaintext_extras').then((r) =>
      this.misc = r.data.map((v, i) =>
        `<li>${Math.floor(i * 4 / 3) + 1}: ${v[0]}</li>`
      ).join('')
    );
  },
}
</script>
