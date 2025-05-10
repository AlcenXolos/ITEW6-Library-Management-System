<template>
  <div class="modal fade show d-block auth-modal">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <!-- HEADER -->
        <div class="modal-header text-white">
          <ul class="nav nav-tabs card-header-tabs w-100">
            <li class="nav-item">
              <a
                class="nav-link text-white"
                :class="{ active: tab==='borrower' }"
                href="#"
                @click.prevent="selectTab('borrower')"
              >
                <i class="fas fa-user-graduate me-1"></i> Borrower
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link text-white"
                :class="{ active: tab==='admin' }"
                href="#"
                @click.prevent="selectTab('admin')"
              >
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
              <i
                :class="tab==='admin'
                  ? 'fas fa-sign-in-alt me-2'
                  : (mode==='login'
                      ? 'fas fa-sign-in-alt me-2'
                      : 'fas fa-user-plus me-2')"
              ></i>
              {{ tab === 'admin'
                ? 'Admin Login'
                : (mode === 'login' ? 'Borrower Login' : 'Register Borrower')
              }}
            </h5>

            <div class="row g-3">
              <!-- First Name (register only) -->
              <div class="col-md-6" v-if="tab==='borrower' && mode==='register'">
                <div class="input-group">
                  <span class="input-group-text"><i class="fas fa-id-badge"></i></span>
                  <input
                    type="text"
                    class="form-control"
                    placeholder="First Name"
                    v-model="firstName"
                    required
                  />
                </div>
              </div>

              <!-- Last Name (register only) -->
              <div class="col-md-6" v-if="tab==='borrower' && mode==='register'">
                <div class="input-group">
                  <span class="input-group-text"><i class="fas fa-id-badge"></i></span>
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Last Name"
                    v-model="lastName"
                    required
                  />
                </div>
              </div>

              <!-- Email (register only) -->
              <div class="col-12" v-if="tab==='borrower' && mode==='register'">
                <div class="input-group">
                  <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                  <input
                    type="email"
                    class="form-control"
                    placeholder="Email"
                    v-model="email"
                    required
                  />
                </div>
              </div>

              <!-- Username -->
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text">
                    <i :class="tab==='admin' ? 'fas fa-user-shield' : 'fas fa-user'"></i>
                  </span>
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Username"
                    v-model="username"
                    required
                  />
                </div>
              </div>

              <!-- Password -->
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text"><i class="fas fa-lock"></i></span>
                  <input
                    type="password"
                    class="form-control"
                    placeholder="Password"
                    v-model="password"
                    required
                  />
                </div>
              </div>

              <!-- Confirm Password (register only) -->
              <div class="col-md-6" v-if="tab==='borrower' && mode==='register'">
                <div class="input-group">
                  <span class="input-group-text"><i class="fas fa-lock"></i></span>
                  <input
                    type="password"
                    class="form-control"
                    placeholder="Confirm Password"
                    v-model="confirmPassword"
                    required
                  />
                </div>
              </div>
            </div>

            <button type="submit" class="btn btn-success w-100 mt-4">
              <i
                :class="tab==='admin'
                  ? 'fas fa-sign-in-alt me-2'
                  : (mode==='login'
                      ? 'fas fa-sign-in-alt me-2'
                      : 'fas fa-user-plus me-2')"
              ></i>
              {{ tab === 'admin'
                  ? 'Login as Admin'
                  : (mode === 'login'
                      ? 'Login as Borrower'
                      : 'Register Borrower')
              }}
            </button>

            <p v-if="tab==='borrower'" class="text-center small mt-3">
              <a href="#" @click.prevent="toggleMode">
                {{ mode === 'login'
                  ? 'New? Create an account'
                  : 'Already registered? Login'
                }}
              </a>
            </p>
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
    const mode = ref('login');
    const username = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const email = ref('');
    const firstName = ref('');
    const lastName = ref('');

    const selectTab = t => {
      tab.value = t;
      mode.value = 'login';
      username.value = password.value = confirmPassword.value = email.value = firstName.value = lastName.value = '';
    };
    const toggleMode = () =>
      (mode.value = mode.value === 'login' ? 'register' : 'login');

    const onSubmit = async () => {
      if (tab.value === 'admin') {
        // only login, no signup for admin
        await store.dispatch('loginUser', {
          username: username.value,
          password: password.value,
          userType: 'admin'
        });
      } else {
        if (mode.value === 'login') {
          await store.dispatch('loginUser', {
            username: username.value,
            password: password.value,
            userType: 'borrower'
          });
        } else {
          // signup
          if (password.value !== confirmPassword.value) {
            return alert('Passwords must match.');
          }
          await store.dispatch('borrowerSignup', {
            username: username.value,
            password: password.value,
            email: email.value,
            first_name: firstName.value,
            last_name: lastName.value
          });
        }
      }
      emit('close');
    };

    return {
      tab, mode, username, password,
      confirmPassword, email, firstName, lastName,
      selectTab, toggleMode, onSubmit
    };
  }
};
</script>