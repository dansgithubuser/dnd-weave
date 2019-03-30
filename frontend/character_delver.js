import Vue from 'vue'
import CharacterDelver from './CharacterDelver.vue'
import store from './store'

Vue.config.productionTip = false

new Vue({
  store,
  render: function (h) { return h(CharacterDelver) }
}).$mount('#character_delver')
