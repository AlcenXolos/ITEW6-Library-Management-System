<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-success px-4">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">CCS112 Group2 Library</router-link>
        <i style="color:white;" class="fa-solid fa-book"></i>
        <div class="collapse navbar-collapse justify-content-end">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Books</router-link>
            </li>
            <li v-if="isBorrower || isAdmin" class="nav-item">
              <router-link class="nav-link" to="/return">Return</router-link>
            </li>
            <li v-if="isAdmin" class="nav-item">
              <router-link class="nav-link" to="/transactions">Transactions</router-link>
            </li>
            <li v-if="isBorrower" class="nav-item">
              <router-link class="nav-link" to="/my-transactions">My Transactions</router-link>
            </li>
            <li v-if="isAdmin" class="nav-item">
              <router-link class="nav-link" to="/add-borrower">Add Borrower</router-link>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-light ms-2" @click="logout" v-if="isLoggedIn">Logout</button>
              <button class="btn btn-light ms-2" @click="showAuth = true" v-else>Login</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <auth-modal v-if="showAuth" @close="showAuth = false" />

    <router-view />
  </div>
</template>

<script>
import AuthModal from './components/AuthModal.vue';
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  components: { AuthModal },
  setup() {
    const store = useStore();
    const router = useRouter();
    const showAuth = ref(false);

    const isLoggedIn = computed(() => store.getters.isLoggedIn);
    const isBorrower = computed(() => store.getters.isBorrower);
    const isAdmin    = computed(() => store.getters.isAdmin);

    const logout = () => {
      store.commit('clearAuth');
      router.push('/');
    };

    // watch login state to close modal + redirect automatically
    store.watch(
      s => s.token,
      t => {
        if (t) {
          showAuth.value = false;
          if (store.getters.isAdmin) router.push('/transactions');
          else router.push('/');
        }
      }
    );

    return { showAuth, isLoggedIn, isBorrower, isAdmin, logout };
  }
};
</script>