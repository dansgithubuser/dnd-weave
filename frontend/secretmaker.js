import Vue from 'vue'
import Secretmaker from './Secretmaker.vue'
import store from './store'

Vue.config.productionTip = false

new Vue({
  store,
  render (h) { return h(Secretmaker) },
}).$mount('#secretmaker')
