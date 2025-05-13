<template>
  <div class="container py-4">
    <h2 class="mb-4"><i class="fas fa-history text-secondary me-2"></i>Transaction History</h2>

    <!-- Filters Row -->
    <div class="row g-3 mb-4 align-items-end">
      <div class="col-md-3">
        <label class="form-label">Search</label>
        <input
          type="text"
          class="form-control"
          placeholder="Search by user, book, or status..."
          v-model="filters.keyword"
        />
      </div>
      <div class="col-md-3">
        <label class="form-label">User</label>
        <select class="form-select" v-model="filters.user">
          <option value="">All Users</option>
          <option v-for="u in uniqueUsers" :key="u" :value="u">{{ u }}</option>
        </select>
      </div>
      <div class="col-md-3">
        <label class="form-label">Book</label>
        <select class="form-select" v-model="filters.book">
          <option value="">All Books</option>
          <option v-for="b in uniqueBooks" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>
      <div class="col-md-3">
        <label class="form-label">Status</label>
        <select class="form-select" v-model="filters.status">
          <option value="">All Statuses</option>
          <option value="borrowed">Borrowed</option>
          <option value="returned">Returned</option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <table class="table table-borderless table-hover align-middle">
      <thead class="table-light">
        <tr>
          <th @click="setSort('index')" style="cursor: pointer;"># <i :class="sortIcon('index')"/></th>
          <th @click="setSort('user.username')" style="cursor: pointer;">User <i :class="sortIcon('user.username')"/></th>
          <th @click="setSort('book.title')" style="cursor: pointer;">Book <i :class="sortIcon('book.title')"/></th>
          <th @click="setSort('status')" style="cursor: pointer;">Status <i :class="sortIcon('status')"/></th>
          <th @click="setSort('borrow_date')" style="cursor: pointer;">Borrowed <i :class="sortIcon('borrow_date')"/></th>
          <th @click="setSort('return_date')" style="cursor: pointer;">Returned <i :class="sortIcon('return_date')"/></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(txn, idx) in paginated" :key="txn.id">
          <td>{{ (currentPage-1)*pageSize + idx + 1 }}</td>
          <td><i class="fas fa-user me-1"></i>{{ txn.user.username }}</td>
          <td><i class="fas fa-book me-1"></i>{{ txn.book.title }}</td>
          <td>
            <span :class="txn.status==='returned' ? 'text-success' : 'text-warning'">
              <i :class="txn.status==='returned' ? 'fas fa-check-circle' : 'fas fa-hourglass-half'" class="me-1"></i>
              {{ txn.status }}
            </span>
          </td>
          <td>{{ formatDate(txn.borrow_date) }}</td>
          <td>{{ txn.return_date ? formatDate(txn.return_date) : '—' }}</td>
        </tr>
        <tr v-if="paginated.length===0">
          <td colspan="6" class="text-center text-muted">No transactions match the selected filters.</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <nav v-if="totalPages > 1">
      <ul class="pagination justify-content-center">
        <li :class="['page-item', { disabled: currentPage===1 }]">
          <button class="page-link" @click="goToPage(currentPage-1)">Previous</button>
        </li>
        <li
          v-for="page in totalPages"
          :key="page"
          :class="['page-item', { active: page===currentPage }]"
        >
          <button class="page-link" @click="goToPage(page)">{{ page }}</button>
        </li>
        <li :class="['page-item', { disabled: currentPage===totalPages }]">
          <button class="page-link" @click="goToPage(currentPage+1)">Next</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';

export default {
  name: 'TransactionHistory',
  setup() {
    const transactions = ref([]);
    const filters = ref({ keyword: '', user: '', book: '', status: '' });
    const sortKey = ref('borrow_date');
    const sortOrder = ref('desc');
    const pageSize = ref(10);
    const currentPage = ref(1);

    const loadTransactions = async () => {
      try {
        const response = await axios.get('/api/transactions/');
        transactions.value = response.data.data;
      } catch (err) {
        console.error('Failed to load transactions', err);
      }
    };

    const uniqueUsers = computed(() => {
      return [...new Set(transactions.value.map(tx => tx.user.username))];
    });
    const uniqueBooks = computed(() => {
      return [...new Set(transactions.value.map(tx => tx.book.title))];
    });

    const filtered = computed(() => {
      return transactions.value.filter(tx => {
        const kw = filters.value.keyword.toLowerCase();
        const matchesKey = [tx.user.username, tx.book.title, tx.status]
          .some(field => field.toLowerCase().includes(kw));
        const matchesUser = filters.value.user ? tx.user.username === filters.value.user : true;
        const matchesBook = filters.value.book ? tx.book.title === filters.value.book : true;
        const matchesStatus = filters.value.status ? tx.status === filters.value.status : true;
        return matchesKey && matchesUser && matchesBook && matchesStatus;
      });
    });

    const sorted = computed(() => {
      return [...filtered.value].sort((a, b) => {
        const get = (obj, path) => path.split('.').reduce((o, k) => o[k], obj);
        const av = get(a, sortKey.value) || '';
        const bv = get(b, sortKey.value) || '';
        if (av < bv) return sortOrder.value === 'asc' ? -1 : 1;
        if (av > bv) return sortOrder.value === 'asc' ? 1 : -1;
        return 0;
      });
    });

    const totalPages = computed(() => Math.ceil(sorted.value.length / pageSize.value));

    const paginated = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      return sorted.value.slice(start, start + pageSize.value);
    });

    function goToPage(n) {
      if (n < 1 || n > totalPages.value) return;
      currentPage.value = n;
    }

    function setSort(key) {
      if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortKey.value = key;
        sortOrder.value = 'asc';
      }
    }

    function sortIcon(key) {
      if (sortKey.value !== key) return '';
      return sortOrder.value === 'asc' ? 'fas fa-sort-up ms-1' : 'fas fa-sort-down ms-1';
    }

    function formatDate(dateStr) {
      if (!dateStr) return '—';
      const d = new Date(dateStr);
      return d.toLocaleString();
    }

    onMounted(loadTransactions);
    return {
      filters,
      uniqueUsers,
      uniqueBooks,
      paginated,
      totalPages,
      currentPage,
      pageSize,
      setSort,
      sortIcon,
      goToPage,
      formatDate
    };
  }
};
</script>

<style scoped>
.table-light th {
  background-color: #5f5f5f;
  color: #fff;
}

/* Override pagination to use success theme */
.pagination .page-link {
  color: #198754;
}
.pagination .page-item .page-link:hover {
  background-color: rgba(25, 135, 84, 0.1);
}
.pagination .page-item.active .page-link {
  background-color: #198754;
  border-color: #198754;
  color: #fff;
}
</style>
