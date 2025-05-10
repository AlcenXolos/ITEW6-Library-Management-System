<template>
  <div class="container py-4">
    <h2>Return a Book</h2>

    <alert-message
      v-if="alert.show"
      :type="alert.type"
      @close="alert.show = false"
    >
      {{ alert.text }}
    </alert-message>

    <table class="table">
      <thead>
        <tr><th>#</th><th>Book</th><th>Borrowed</th><th>Action</th></tr>
      </thead>
      <tbody>
        <tr v-for="(t, i) in pending" :key="t.id">
          <td>{{ i + 1 }}</td>
          <td>{{ t.book.title }}</td>
          <td>{{ new Date(t.borrow_date).toLocaleDateString() }}</td>
          <td>
            <button
              class="btn btn-success btn-sm"
              @click="ret(t.id)"
            >Return</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default {
  setup() {
    const store = useStore();
    const username = computed(() => store.getters.username);
    const pending = ref([]);
    const alert   = ref({ show:false, type:'', text:'' });

    // load only borrowed transactions for this user (or all if admin)
    async function load() {
      try {
        const url = `/api/transactions/?user=${username.value}&status=borrowed`;
        const res = await axios.get(url);
        // our build_response wraps actual list in res.data.data
        pending.value = res.data.data;
      } catch (e) {
        console.error(e);
      }
    }

    async function ret(id) {
      try {
        const res = await axios.post(`/api/return/${id}/`);
        alert.value = {
          show: true,
          type: 'success',
          text: res.data.message
        };
        // remove from list immediately
        pending.value = pending.value.filter(t => t.id !== id);
      } catch (e) {
        const msg = e.response?.data?.message || 'Return failed.';
        alert.value = { show: true, type: 'danger', text: msg };
      }
    }

    onMounted(load);
    return { pending, alert, ret };
  }
};
</script>
