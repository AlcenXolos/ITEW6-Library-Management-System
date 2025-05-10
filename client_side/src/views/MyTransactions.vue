<template>
  <div class="container py-4">
    <h2>My Transactions</h2>
    <table class="table table-hover">
      <thead class="table-light">
        <tr>
          <th>#</th>
          <th>Book</th>
          <th>Status</th>
          <th>Borrowed</th>
          <th>Returned</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(t,i) in txns" :key="t.id">
          <td>{{ i+1 }}</td>
          <td>{{ t.book }}</td>
          <td>
            <span :class="t.status==='returned' ? 'text-success' : 'text-warning'">
              {{ t.status }}
            </span>
          </td>
          <td>{{ t.borrow_date }}</td>
          <td>{{ t.return_date || '—' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
export default {
  setup() {
    const txns = ref([]);
    onMounted(async () => {
      // stub GET /api/transactions/?user=…
      txns.value = [
        { id:1, book:'1984', status:'returned', borrow_date:'2024-04-20', return_date:'2024-04-25' },
        { id:2, book:'Brave New World', status:'borrowed', borrow_date:'2024-05-01', return_date:null }
      ];
    });
    return { txns };
  }
};
</script>