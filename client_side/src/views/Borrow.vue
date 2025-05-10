<!-- <template>
  <div class="container py-4">
    <h2>Borrow a Book</h2>
    <alert-message v-if="alert.show" :type="alert.type" @close="alert.show=false">
      {{ alert.text }}
    </alert-message>
    <form @submit.prevent="borrow">
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <select v-model="form.bookId" class="form-select" :class="{ 'is-invalid': errors.bookId }">
            <option value="">Select Book…</option>
            <option v-for="b in books" :key="b.id" :value="b.id">
              {{ b.title }} ({{ b.copies_available }})
            </option>
          </select>
          <div class="invalid-feedback">{{ errors.bookId }}</div>
        </div>
        <div class="col-md-6">
          <input
            v-model="form.username"
            class="form-control"
            placeholder="Your Username"
            :class="{ 'is-invalid': errors.username }"
          />
          <div class="invalid-feedback">{{ errors.username }}</div>
        </div>
      </div>
      <button class="btn btn-success">Borrow</button>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
export default {
  setup() {
    const books = ref([]);
    const form = ref({ bookId:'', username:'' });
    const errors = ref({});
    const alert = ref({ show:false, type:'', text:'' });

    onMounted(async()=> books.value = await fetch('http://localhost:8000/books/').then(r=>r.json()) );

    function validate() {
      errors.value = {};
      if (!form.value.bookId) errors.value.bookId = 'Choose a book.';
      if (!form.value.username) errors.value.username = 'Enter your username.';
      return !Object.keys(errors.value).length;
    }

    async function borrow() {
      if (!validate()) return;
      try {
        // stub POST /borrow/
        await fetch('http://localhost:8000/borrow/', {
          method:'post',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify(form.value)
        });
        alert.value = { show:true, type:'success', text:'Book borrowed!' };
        form.value.bookId = form.value.username = '';
      } catch {
        alert.value = { show:true, type:'danger', text:'Could not borrow.' };
      }
    }

    return { books, form, errors, alert, borrow };
  }
};
</script> -->