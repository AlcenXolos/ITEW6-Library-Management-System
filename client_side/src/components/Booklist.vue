<template>
  <div class="container py-4">
    <div class="d-flex align-items-center mb-4">
      <h2 class="me-auto">Books</h2>
      <button v-if="isAdmin" class="btn btn-success" @click="openForm('Add')">
        <i class="fas fa-plus me-2"></i>Add Book
      </button>
    </div>

    <alert-message v-if="alert.show" :type="alert.type" @close="alert.show = false">
      {{ alert.text }}
    </alert-message>

    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="b in books" :key="b.id">
        <div class="card h-100 position-relative card-hover overflow-hidden">
          <!-- Copies badge top right -->
          <span class="badge bg-primary position-absolute top-0 end-0 m-2">
            <i class="fas fa-layer-group me-1"></i>{{ b.copies_available }}
          </span>

          <div class="card-body d-flex flex-column">
            <h5 class="card-title mb-2">{{ b.title }}</h5>
            <p class="card-text text-secondary mb-4">by {{ b.author }}</p>
            <div class="mt-auto d-flex gap-2">
              <button v-if="isAdmin" class="btn btn-outline-secondary btn-sm flex-fill" @click="openForm('Edit', b)"
                title="Edit Book">
                <i class="fas fa-edit"></i>
              </button>
              <button v-if="isAdmin" class="btn btn-outline-danger btn-sm flex-fill" @click="confirmDelete(b.id)"
                title="Delete Book">
                <i class="fas fa-trash"></i>
              </button>
              <button v-if="isLoggedIn && canBorrow" class="btn btn-success flex-fill"
                :disabled="b.copies_available === 0" @click="borrow(b)" title="Borrow Book">
                <i class="fas fa-cart-plus me-1"></i>Borrow
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <BookForm v-model:show="formVisible" :mode="formMode" :book="selectedBook" @saved="onSaved" />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import BookForm from './BookForm.vue';
import AlertMessage from './AlertMessage.vue';

export default {
  name: 'BookList',
  components: { BookForm, AlertMessage },
  props: ['canBorrow'],
  setup() {
    const store = useStore();
    const books = ref([]);
    const formVisible = ref(false);
    const formMode = ref('Add');
    const selectedBook = ref({});
    const alert = ref({ show: false, type: '', text: '' });

    const isLoggedIn = computed(() => store.getters.isLoggedIn);
    const isAdmin = computed(() => store.getters.isAdmin);

    const reload = async () => {
      try {
        const { data } = await axios.get('/api/books/');
        books.value = data;
      } catch {
        alert.value = { show: true, type: 'danger', text: 'Failed to load books.' };
      }
    };

    const openForm = (mode, book = {}) => {
      formMode.value = mode;
      selectedBook.value = book;
      formVisible.value = true;
    };

    const confirmDelete = async (id) => {
      if (!confirm('Delete this book?')) return;
      try {
        await axios.delete(`/api/books/${id}/delete/`);
        books.value = books.value.filter(b => b.id !== id);
        alert.value = { show: true, type: 'warning', text: 'Book deleted succesfully.' };
      } catch (err) {
        let errorMessage = 'Delete failed.';
        if (err.response && err.response.data && err.response.data.detail) {
          errorMessage = err.response.data.detail;
        }
        alert.value = { show: true, type: 'danger', text: errorMessage };
      }
    };

    const borrow = async (book) => {
      // if (!store.getters.isBorrower) {
      //   alert.value = { show: true, type: 'warning', text: 'Please log in as borrower.' };
      //   return;
      // }
      try {
        await axios.post('/api/borrow/', { book_id: book.id });
        book.copies_available--;
        alert.value = { show: true, type: 'success', text: `Borrowed “${book.title}”!` };
      } catch (err) {
        let msg = 'Borrow failed.';
        const resp = err.response?.data;
        if (resp?.message) msg = resp.message;
        alert.value = { show: true, type: 'warning', text: msg };
      }
    };

    const onSaved = async () => {
      await reload();
      alert.value = {
        show: true,
        type: 'success',
        text: formMode.value === 'Add' ? 'Book added!' : 'Book updated!'
      };
    };

    onMounted(reload);

    return {
      books,
      formVisible,
      formMode,
      selectedBook,
      isLoggedIn,
      isAdmin,
      alert,
      openForm,
      confirmDelete,
      borrow,
      onSaved
    };
  }
};
</script>

<style scoped>
.card-hover {
  transition: transform .2s, box-shadow .2s;
}

.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}
</style>