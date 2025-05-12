<template>
  <div class="container py-4">
    <h2 class="mb-4">
      <i class="fas fa-history text-secondary me-2"></i>Transaction History
    </h2>

    <!-- Search input -->
    <div class="mb-3">
      <div class="w-50">
        <label for="userSearch" class="form-label">Search:</label>
        <input
          id="userSearch"
          type="text"
          class="form-control"
          placeholder="Search by user, book, or status..."
          v-model="userSearch"
        />
      </div>
    </div>

    <table class="table table-borderless table-hover align-middle">
      <thead class="table-light">
        <tr>
          <th>#</th>
          <th>User</th>
          <th>Book</th>
          <th>Status</th>
          <th>Borrowed</th>
          <th>Returned</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(txn, i) in filteredTransactions"
          :key="i"
        >
          <td>{{ i + 1 }}</td>
          <td><i class="fas fa-user me-1"></i>{{ txn.user.username }}</td>
          <td><i class="fas fa-book me-1"></i>{{ txn.book.title }}</td>
          <td>
            <span :class="txn.status === 'returned' ? 'text-success' : 'text-warning'">
              <i
                :class="txn.status === 'returned'
                  ? 'fas fa-check-circle'
                  : 'fas fa-hourglass-half'"
                class="me-1"
              ></i>
              {{ txn.status }}
            </span>
          </td>
          <td>{{ formatDate(txn.borrow_date) }}</td>
          <td>{{ formatDate(txn.return_date) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import { onMounted, ref, computed } from 'vue';

export default {
  setup() {
    const transactions = ref([]);
    const users = ref([]);
    const userSearch = ref('');


    const loadTransactions = async () => {
      try {
        const response = await axios.get('/api/transactions/');
        transactions.value = response.data.data;
      } catch (err) {
        console.error('Failed to load transactions', err);
      }
    };

    const loadUsers = async () => {
      try {
        const response = await axios.get('/api/borrowers/');
        users.value = response.data.data;
      } catch (err) {
        console.error('Failed to load users', err);
      }
    };
    const formatDate = (dateStr) => {
      if (!dateStr) return '—';
      const date = new Date(dateStr);
      return date.toLocaleString('en-US', {
        month: 'short',    
        day: '2-digit',    
        year: 'numeric',   
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true       // 12-hour format with AM/PM
      });
    };

    const filteredTransactions = computed(() => {
    const keyword = userSearch.value.trim().toLowerCase();

      return transactions.value.filter(txn => {
        return (
          txn.user.username.toLowerCase().includes(keyword) ||
          txn.book.title.toLowerCase().includes(keyword) ||
          txn.status.toLowerCase().includes(keyword)
        );
      });
    });


    onMounted(() => {
      loadTransactions();
      loadUsers();
    });

    return {
      transactions,
      users,
      userSearch,
      filteredTransactions,
      formatDate
    };
  }
};
</script>
