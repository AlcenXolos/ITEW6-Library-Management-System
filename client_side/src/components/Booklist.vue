<template>
  <div class="container py-4">
    <!-- Header with Add Book button for Admin -->
    <div class="d-flex align-items-center mb-3">
      <h2 class="me-auto">Books</h2>
      <button
        v-if="isAdmin"
        class="btn btn-success"
        @click="openForm('Add')"
      >
        <i class="fas fa-plus me-1"></i> Add Book
      </button>
    </div>

    <!-- Alert Messages -->
    <alert-message
      v-if="alert.show"
      :type="alert.type"
      @close="alert.show = false"
    >
      {{ alert.text }}
    </alert-message>

    <!-- Book Cards -->
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="book in books" :key="book.id">
        <div class="card h-100 card-hover border-0">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ book.title }}</h5>
            <p class="card-text text-muted">{{ book.author }}</p>
            <small class="badge bg-info text-dark mb-3">
              <i class="fas fa-layer-group me-1"></i>
              {{ book.copies_available }}
            </small>
            <div class="mt-auto d-flex gap-2">
              <!-- Edit/Delete for Admin -->
              <button
                v-if="isAdmin"
                class="btn btn-outline-secondary btn-sm flex-fill"
                @click="openForm('Edit', book)"
              ><i class="fas fa-edit"></i></button>
              <button
                v-if="isAdmin"
                class="btn btn-outline-danger btn-sm flex-fill"
                @click="confirmDelete(book.id)"
              ><i class="fas fa-trash"></i></button>
              <!-- Borrow for Borrower -->
              <button
                v-if="canBorrow"
                class="btn btn-success flex-fill"
                :disabled="book.copies_available === 0"
                @click="borrow(book)"
              >
                <i class="fas fa-cart-plus me-1"></i> Borrow
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Book Add/Edit Modal -->
    <BookForm
      v-model:show="formVisible"
      :mode="formMode"
      :book="selectedBook"
      @saved="reload"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import BookForm from './BookForm.vue';
import AlertMessage from './AlertMessage.vue';

export default {
  name: 'BookList',
  components: { BookForm, AlertMessage },
  props: ['canBorrow'],
  setup(props) {
    const store = useStore();
    const books = ref([]);
    const formVisible = ref(false);
    const formMode = ref('Add');
    const selectedBook = ref({});
    const alert = ref({ show: false, type: '', text: '' });

    const isAdmin = computed(() => store.getters.isAdmin);
    const username = computed(() => store.getters.username);

    // Load book list
    async function reload() {
      try {
        const res = await fetch('http://localhost:8000/books/');
        books.value = await res.json();
      } catch (e) {
        alert.value = { show: true, type: 'danger', text: 'Failed to fetch books.' };
      }
    }

    // Open Add/Edit modal
    function openForm(mode, book = {}) {
      formMode.value = mode;
      selectedBook.value = book;
      formVisible.value = true;
    }

    // Delete a book
    async function confirmDelete(id) {
      if (!confirm('Delete this book?')) return;
      try {
        await fetch(`http://localhost:8000/books/${id}/`, { method: 'DELETE' });
        books.value = books.value.filter(b => b.id !== id);
        alert.value = { show: true, type: 'warning', text: 'Book deleted.' };
      } catch {
        alert.value = { show: true, type: 'danger', text: 'Delete failed.' };
      }
    }

    // Borrow a book inline
    async function borrow(book) {
      if (!store.getters.isBorrower) {
        alert.value = { show: true, type: 'warning', text: 'Please log in as borrower.' };
        return;
      }
      try {
        await fetch('http://localhost:8000/borrow/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user: username.value, book_id: book.id })
        });
        book.copies_available--;
        alert.value = { show: true, type: 'success', text: `You borrowed “${book.title}”!` };
      } catch {
        alert.value = { show: true, type: 'danger', text: 'Borrow failed.' };
      }
    }

    onMounted(reload);

    return {
      books,
      formVisible,
      formMode,
      selectedBook,
      isAdmin,
      alert,
      openForm,
      confirmDelete,
      borrow
    };
  }
};
</script>