import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faLinkedin, faTwitter } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTwitter)
library.add(faLinkedin)

Vue.config.productionTip = false
Vue.component('font-awesome-icon', FontAwesomeIcon)


new Vue({
  render: h => h(App),
}).$mount('#app')
