<template>
  <div class="modal fade show d-block auth-modal">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <!-- HEADER -->
        <div class="modal-header text-white">
          <ul class="nav nav-tabs card-header-tabs w-100">
            <li class="nav-item">
              <a class="nav-link text-white" :class="{ active: tab === 'borrower' }" href="#"
                @click.prevent="selectTab('borrower')">
                <i class="fas fa-user-graduate me-1"></i> Borrower
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link text-white" :class="{ active: tab === 'admin' }" href="#"
                @click.prevent="selectTab('admin')">
                <i class="fas fa-user-shield me-1"></i> Admin
              </a>
            </li>
          </ul>
          <button type="button" class="btn-close btn-close-white" @click="$emit('close')" />
        </div>

        <!-- BODY -->
        <div class="modal-body px-5 py-4">
          <form @submit.prevent="onSubmit">
            <h5 class="mb-4">
              <i class="fas fa-sign-in-alt me-2"></i>
              {{ tab === 'admin' ? 'Admin Login' : 'Borrower Login' }}
            </h5>

            <div class="row g-3">
              <!-- Username -->
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text">
                    <i :class="tab === 'admin' ? 'fas fa-user-shield' : 'fas fa-user'"></i>
                  </span>
                  <input type="text" class="form-control" placeholder="Username" v-model="username" required />
                </div>
              </div>

              <!-- Password -->
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text"><i class="fas fa-lock"></i></span>
                  <input type="password" class="form-control" placeholder="Password" v-model="password" required />
                </div>
              </div>
            </div>

            <button type="submit" class="btn btn-success w-100 mt-4">
              <i class="fas fa-sign-in-alt me-2"></i>
              {{ tab === 'admin' ? 'Login as Admin' : 'Login as Borrower' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';

export default {
  emits: ['close'],
  setup(_, { emit }) {
    const store = useStore();

    const tab = ref('borrower');
    const username = ref('');
    const password = ref('');

    const selectTab = (t) => {
      tab.value = t;
      username.value = '';
      password.value = '';
    };

    const onSubmit = async () => {
      await store.dispatch('loginUser', {
        username: username.value,
        password: password.value
      });

      if (tab.value === 'admin') {
        if (!store.getters.isAdmin) {
          store.commit('clearAuth');
          return alert('Invalid credentials for Admin.');
        }
      } else {
        if (!store.getters.isBorrower) {
          return alert('Logged in as an Admin. You can still borrow books.');
        }
      }

      emit('close');
    };

    return {
      tab,
      username,
      password,
      selectTab,
      onSubmit
    };
  }
};
</script>

<style scoped>
.auth-modal {
  background-color: rgba(0, 0, 0, 0.6);
}
</style>
