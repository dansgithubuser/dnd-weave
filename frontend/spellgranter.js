import Vue from 'vue'
import Spellgranter from './Spellgranter.vue'
import store from './store'

Vue.config.productionTip = false

new Vue({
  store,
  render (h) { return h(Spellgranter) },
}).$mount('#spellgranter')
