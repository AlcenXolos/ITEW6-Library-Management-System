<template>
  <div style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif" class="container py-4">
    <h2 style="font-size: 50px;">My Transactions  <i class="fa-solid fa-rectangle-list"></i></h2>
    <alert-message
      v-if="alert.show"
      :type="alert.type"
      @close="alert.show=false"
    >
      {{ alert.text }}
    </alert-message>

    <table class="table table-hover">
      <thead class="table-light">
        <tr>
          <th style="background-color: #5f5f5f; color: white;">#</th>
          <th style="background-color: #5f5f5f; color: white;">Book</th>
          <th style="background-color: #5f5f5f; color: white;">Status</th>
          <th style="background-color: #5f5f5f; color: white;">Borrowed</th>
          <th style="background-color: #5f5f5f; color: white;">Returned</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(t, i) in txns" :key="t.id">
          <td>{{ i + 1 }}</td>
          <td><i class="fas fa-book me-1"></i>{{ t.book.title }}</td>
          <td>
            <span :class="t.status === 'returned' ? 'text-success' : 'text-warning'">
              <i
                :class="t.status === 'returned'
                  ? 'fas fa-check-circle'
                  : 'fas fa-hourglass-half'"
                class="me-1"
              ></i>
              {{ t.status }}
            </span>
          </td>
          <td>{{ formatDate(t.borrow_date) }}</td>
          <td>{{ t.return_date ? formatDate(t.return_date) : '—' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import AlertMessage from '../components/AlertMessage.vue';

export default {
  components: { AlertMessage },
  setup() {
    const txns = ref([]);
    const alert = ref({ show: false, type: '', text: '' });

    // Fetch only this user's transactions
    const load = async () => {
      try {
        const res = await axios.get('/api/transactions/');
        txns.value = res.data.data;
      } catch (e) {
        console.error('Failed to load transactions', e);
        alert.value = { show: true, type: 'danger', text: 'Failed to load your transactions.' };
      }
    };

    // Helper to format dates
    const formatDate = (iso) => new Date(iso).toLocaleDateString();

    onMounted(load);
    return { txns, alert, formatDate };
  }
};
</script>