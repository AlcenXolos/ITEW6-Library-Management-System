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
          <alert-message
            v-if="alert.show"
            :type="alert.type"
            @close="alert.show = false"
          >
            {{ alert.message }}
          </alert-message>

          <form @submit.prevent="onSubmit">
            <h5 class="mb-4">
              <i class="fas fa-sign-in-alt me-2"></i>
              {{ tab === 'admin' ? 'Admin Login' : 'Borrower Login' }}
            </h5>

            <div class="row g-3">
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text">
                    <i :class="tab==='admin' ? 'fas fa-user-shield' : 'fas fa-user'"></i>
                  </span>
                  <input
                    v-model="username"
                    type="text"
                    class="form-control"
                    placeholder="Username"
                    required
                  />
                </div>
              </div>
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="fas fa-lock"></i>
                  </span>
                  <input
                    v-model="password"
                    type="password"
                    class="form-control"
                    placeholder="Password"
                    required
                  />
                </div>
              </div>
            </div>

            <button type="submit" class="btn btn-success w-100 mt-4">
              <i class="fas fa-sign-in-alt me-2"></i>
              {{ tab==='admin' ? 'Login as Admin' : 'Login as Borrower' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { login as loginService } from '@/services/authService'
import AlertMessage from './AlertMessage.vue'

export default {
  components: { AlertMessage },
  emits: ['close'],
  setup(_, { emit }) {
    const store   = useStore()
    const router  = useRouter()
    const tab      = ref('borrower')
    const username = ref('')
    const password = ref('')
    const alert    = ref({ show:false, type:'danger', message:'' })

    function selectTab(t) {
      tab.value = t
      username.value = password.value = ''
      alert.value.show = false
    }

    async function onSubmit() {
      alert.value.show = false

      try {
        // 1) call DRF /login/
        const { token, is_staff, username: respUser } = await loginService({
          username: username.value.trim(),
          password: password.value
        })

        // 2) role checks *before* committing
        if (tab.value==='admin' && !is_staff) {
          throw new Error('You do not have permission to log in as Admin.')
        }

        // 3) commit the token & userType
        store.commit('setAuth', {
          token,
          userType: is_staff ? 'admin' : 'borrower',
          username: respUser
        })

        // 4) if you logged in as Admin from Borrower tab
        if (tab.value==='borrower' && is_staff) {
            window.alert('You logged in as Admin. You can still borrow books.')
            emit('close')
            router.push('/')
            return
        }

        // 5) successful login for your selected tab
        emit('close')
        router.push(tab.value==='admin' ? '/transactions' : '/')
      }
      catch (err) {
        // pull out DRF errors or our thrown message
        let msg = 'Login failed.'
        const resp = err.response?.data || {}
        if (Array.isArray(resp.non_field_errors)) {
          msg = resp.non_field_errors[0]
        }
        else if (resp.detail) {
          msg = resp.detail
        }
        else if (err.message) {
          msg = err.message
        }

        alert.value = { show:true, type:'danger', message: msg }
      }
    }

    return {
      tab, username, password, alert,
      selectTab, onSubmit
    }
  }
}
</script>

<style scoped>
.auth-modal { background-color: rgba(0,0,0,0.6); }
</style>
