<template>
  <div class="container py-4">
    <h2>Return a Book</h2>
    <alert-message v-if="alert.show" :type="alert.type" @close="alert.show=false">
      {{ alert.text }}
    </alert-message>
    <table class="table">
      <thead><tr>
        <th>#</th><th>Book</th><th>Borrowed</th><th>Action</th>
      </tr></thead>
      <tbody>
        <tr v-for="(t,i) in pending" :key="t.id">
          <td>{{ i+1 }}</td>
          <td>{{ t.book }}</td>
          <td>{{ t.borrow_date }}</td>
          <td>
            <button class="btn btn-success btn-sm" @click="ret(t.id)">Return</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';

export default {
  setup() {
    const store = useStore();
    const username = computed(() => store.getters.username);
    const pending = ref([]);
    const alert   = ref({ show:false, type:'', text:'' });

    async function load() {
      pending.value = await fetch(
        `http://localhost:8000/api/transactions?user=${username.value}&status=borrowed`
      ).then(r=>r.json());
    }

    async function ret(id) {
      try {
        await fetch(`http://localhost:8000/return/${id}/`, { method:'POST' });
        alert.value = { show:true, type:'success', text:'Book returned!' };
        pending.value = pending.value.filter(t=>t.id!==id);
      } catch {
        alert.value = { show:true, type:'danger', text:'Return failed.' };
      }
    }

    onMounted(load);
    return { pending, alert, ret };
  }
};
</script>