<template>
  <div style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif" class="container py-4">
    <h2 style="font-size: 50px;">Return a Book  <i class="fa-solid fa-rotate-left"></i></h2>

    <alert-message
      v-if="alert.show"
      :type="alert.type"
      @close="alert.show = false"
    >
      {{ alert.text }}
    </alert-message>

   <div v-if="pending.length > 0">
      <table class="table">
        <thead>
          <tr>
            <th style="background-color: #5f5f5f; color: white;">#</th>
            <th style="background-color: #5f5f5f; color: white;">Book</th>
            <th style="background-color: #5f5f5f; color: white;">Borrowed</th>
            <th style="background-color: #5f5f5f; color: white;">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(t, i) in pending" :key="t.id">
            <td>{{ i + 1 }}</td>
            <td>{{ t.book.title }}</td>
            <td>{{ formatDate(t.borrow_date) }}</td>
            <td>
              <button
                class="btn btn-success btn-sm"
                @click="openConfirm(t)"
              >Return</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="text-center mt-4" style="font-size: 20px; color: #6a9f4a;">
      You have no books to return.
    </p>

    <!-- Confirmation Modal -->
    <div 
      v-if="confirmVisible" 
      class="modal-backdrop fade show"
    ></div>
    <div 
      v-if="confirmVisible" 
      class="modal fade show d-block" 
      tabindex="-1" 
      aria-modal="true" 
      role="dialog"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Return</h5>
            <button type="button" class="btn-close" @click="confirmVisible = false"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to return this book?</p>
            <ul class="list-unstyled">
              <li><strong>Book:</strong> {{ selected.book.title }}</li>
              <li><strong>ISBN:</strong> {{ selected.book.isbn }}</li>
              <li><strong>Borrowed On:</strong> {{ formatDate(selected.borrow_date) }}</li>
              <li><strong>Return Date:</strong> {{ formatDate(currentDate) }}</li>
            </ul>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="confirmVisible = false">
              Cancel
            </button>
            <button class="btn btn-success" @click="confirmReturn">
              Yes, Return
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import AlertMessage from '@/components/AlertMessage.vue';

export default {
  components: { AlertMessage },
  setup() {
    const store = useStore();
    const username = computed(() => store.getters.username);
    const pending = ref([]);
    const alert   = ref({ show:false, type:'', text:'' });

    const confirmVisible = ref(false);
    const selected = ref({});          // currently‐selected transaction
    const currentDate = new Date();     // used in modal

    // load only borrowed transactions for this user (or all if admin)
    async function load() {
      try {
        const url = `/api/transactions/?user=${username.value}&status=borrowed`;
        const res = await axios.get(url);
        pending.value = res.data.data;
      } catch (e) {
        console.error(e);
        alert.value = { show:true, type:'danger', text:'Failed to load pending transactions.' };
      }
    }

    function openConfirm(txn) {
      selected.value = txn;
      confirmVisible.value = true;
    }

    async function confirmReturn() {
      try {
        const res = await axios.post(`/api/return/${selected.value.id}/`);
        alert.value = {
          show: true,
          type: 'success',
          text: res.data.message || 'Book returned successfully.'
        };
        // remove returned item
        pending.value = pending.value.filter(t => t.id !== selected.value.id);
      } catch (e) {
        const msg = e.response?.data?.message || 'Return failed.';
        alert.value = { show:true, type:'danger', text: msg };
      } finally {
        confirmVisible.value = false;
      }
    }

    function formatDate(dt) {
      return new Date(dt).toLocaleDateString();
    }

    onMounted(load);
    return {
      pending,
      alert,
      currentDate,
      confirmVisible,
      selected,
      openConfirm,
      confirmReturn,
      formatDate
    };
  }
};
</script>

<style scoped>
.modal-backdrop {
  z-index: 1040;
}
.modal {
  z-index: 1050;
}
</style>
