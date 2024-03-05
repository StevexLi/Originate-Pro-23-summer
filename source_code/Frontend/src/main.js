import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

//3
import NgFormElementPlus  from 'ng-form-elementplus'
import 'ng-form-elementplus/lib/style.css'

const app = createApp(App)
app.use(store).use(router).use(ElementPlus).use(NgFormElementPlus).mount('#app')
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
