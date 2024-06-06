import { createStore } from 'vuex'

export default createStore({
  state: {
    login:false
  },
  getters: {
  },
  mutations: {
    logged_in(state){
      state.login = true
    }
  },
  actions: {
  },
  modules: {
  }
})
