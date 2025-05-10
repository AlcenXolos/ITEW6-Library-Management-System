<template>
  <div class="container py-4">
    <h2 class="mb-4"><i class="fas fa-history text-secondary me-2"></i>Transaction History</h2>
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
        <tr v-for="(txn,i) in transactions" :key="i">
          <td>{{ i+1 }}</td>
          <td><i class="fas fa-user me-1"></i>{{ txn.user }}</td>
          <td><i class="fas fa-book me-1"></i>{{ txn.book }}</td>
          <td>
            <span
              :class="txn.status==='returned' ? 'text-success' : 'text-warning'"
            >
              <i
                :class="txn.status==='returned'
                  ? 'fas fa-check-circle'
                  : 'fas fa-hourglass-half'"
                class="me-1"
              ></i>
              {{ txn.status }}
            </span>
          </td>
          <td>{{ txn.borrow_date }}</td>
          <td>{{ txn.return_date || '—' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import { onMounted, ref } from 'vue';

export default {
  setup() {
    const transactions = ref([]);

    const loadTransactions = async () => {
      try {
        // Replace with real API if available
        // const response = await axios.get('http://localhost:8000/api/transactions/');
        transactions.value = [
          {
            user: 'john_doe',
            book: '1984',
            status: 'returned',
            borrow_date: '2024-04-20',
            return_date: '2024-04-25'
          },
          {
            user: 'alice',
            book: 'Brave New World',
            status: 'borrowed',
            borrow_date: '2024-05-01',
            return_date: null
          }
        ];
      } catch (err) {
        console.error('Failed to load transactions', err);
      }
    };

    onMounted(loadTransactions);
    return { transactions };
  }
};
</script>