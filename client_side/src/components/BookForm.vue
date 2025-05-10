<template>
  <div v-if="show">
    <div class="modal-backdrop fade show"></div>
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ mode }} Book</h5>
            <button class="btn-close" @click="$emit('update:show', false)"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleSubmit" novalidate>
              <div class="mb-3">
                <label class="form-label">Title</label>
                <input
                  v-model="form.title"
                  :class="['form-control', errors.title && 'is-invalid']"
                />
                <div class="invalid-feedback">{{ errors.title }}</div>
              </div>
              <div class="mb-3">
                <label class="form-label">Author</label>
                <input
                  v-model="form.author"
                  :class="['form-control', errors.author && 'is-invalid']"
                />
                <div class="invalid-feedback">{{ errors.author }}</div>
              </div>
              <div class="mb-3">
                <label class="form-label">ISBN</label>
                <input
                  v-model="form.isbn"
                  :class="['form-control', errors.isbn && 'is-invalid']"
                />
                <div class="invalid-feedback">{{ errors.isbn }}</div>
              </div>
              <div class="mb-3">
                <label class="form-label">Copies Available</label>
                <input
                  type="number"
                  v-model.number="form.copies_available"
                  :class="['form-control', errors.copies_available && 'is-invalid']"
                />
                <div class="invalid-feedback">{{ errors.copies_available }}</div>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="$emit('update:show', false)">
                  Cancel
                </button>
                <button type="submit" class="btn btn-success">
                  {{ mode === 'Add' ? 'Create' : 'Save' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import axios from 'axios';

export default {
  props: {
    show: Boolean,
    mode: { type: String, default: 'Add' },
    book: {
      type: Object,
      default: () => ({ id: null, title: '', author: '', isbn: '', copies_available: 0 })
    }
  },
  emits: ['update:show', 'saved'],
  setup(props, { emit }) {
    const form = ref({ ...props.book });
    const errors = ref({});

    watch(
      () => props.book,
      (b) => {
        form.value = { ...b };
        errors.value = {};
      }
    );

    function validate() {
      errors.value = {};
      if (!form.value.title) errors.value.title = 'Title is required.';
      if (!form.value.author) errors.value.author = 'Author is required.';
      if (!form.value.isbn) errors.value.isbn = 'ISBN is required.';
      else if (!/^\d{10,13}$/.test(form.value.isbn))
        errors.value.isbn = 'ISBN must be 10–13 digits.';
      if (form.value.copies_available < 0)
        errors.value.copies_available = 'Must be zero or more.';
      return !Object.keys(errors.value).length;
    }

    async function handleSubmit() {
      if (!validate()) return;
      try {
        if (props.mode === 'Add') {
          await axios.post('/api/books/add/', form.value);
        } else {
          await axios.put(`/api/books/${form.value.id}/`, form.value);
        }
        emit('saved');
        emit('update:show', false);
      } catch (e) {
        // map backend errors if you like, or alert
        alert('Operation failed. See console.');
        console.error(e.response?.data || e);
      }
    }

    return { form, errors, handleSubmit };
  }
};
</script>

<style scoped>
/* prevent a scroll jump when modal opens */
body.modal-open {
  overflow: hidden;
}
</style>