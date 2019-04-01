import Vue from 'vue'
import PlaintextExplorer from './PlaintextExplorer.vue'
import store from './store'

Vue.config.productionTip = false

new Vue({
  store,
  render (h) { return h(PlaintextExplorer) },
}).$mount('#plaintext_explorer')
