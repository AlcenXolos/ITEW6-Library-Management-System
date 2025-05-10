import { createStore } from 'vuex';

export default createStore({
  state: {
    userType: null,     // 'admin' | 'borrower' | null
    username: null      // store the borrower’s username
  },
  mutations: {
    login(state, payload) {
      // payload = { userType: 'borrower' | 'admin', username: '…' }
      state.userType = payload.userType;
      state.username = payload.username || null;
    },
    logout(state) {
      state.userType = null;
      state.username = null;
    }
  },
  getters: {
    isLoggedIn: state => state.userType !== null,
    isAdmin:    state => state.userType === 'admin',
    isBorrower: state => state.userType === 'borrower',
    username:   state => state.username
  }
});