// This is a declaration for comonents that like to be difficult, it tells ts that all .vue files are ts
// src/vue.d.ts
declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}