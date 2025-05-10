// src/store/index.js
import { createStore } from 'vuex'
import axios from 'axios'
import { login, signupBorrower } from '@/services/authService'

const savedToken    = localStorage.getItem('token')
const savedUser    = localStorage.getItem('userType')
const savedUsername = localStorage.getItem('username')

if (savedToken) {
  axios.defaults.headers.common['Authorization'] = `Token ${savedToken}`
}

export default createStore({
  state: {
    token:     savedToken || null,
    userType:  savedUser  || null,   // 'admin' | 'borrower'
    username:  savedUsername || null
  },
  mutations: {
    setAuth(state, { token, userType, username }) {
      state.token    = token
      state.userType = userType
      state.username = username
      axios.defaults.headers.common['Authorization'] = `Token ${token}`

      localStorage.setItem('token', token)
      localStorage.setItem('userType', userType)
      localStorage.setItem('username', username)
    },
    clearAuth(state) {
      state.token    = null
      state.userType = null
      state.username = null
      delete axios.defaults.headers.common['Authorization']

      localStorage.removeItem('token')
      localStorage.removeItem('userType')
      localStorage.removeItem('username')
    }
  },
  actions: {
    async borrowerSignup({ dispatch }, payload) {
      await signupBorrower(payload)
      return dispatch('loginUser', { ...payload, userType: 'borrower' })
    },
    async loginUser({ commit }, { username, password, userType }) {
      const data = await login({ username, password })
      commit('setAuth', {
        token:    data.token,
        userType,
        username
      })
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    isAdmin:    state => state.userType === 'admin',
    isBorrower: state => state.userType === 'borrower',
    username:   state => state.username
  }
})