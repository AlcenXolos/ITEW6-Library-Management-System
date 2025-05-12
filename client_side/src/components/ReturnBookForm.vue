<template>
    <div class="modal fade show d-block" tabindex="-1" style="background:rgba(0,0,0,0.5);">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">Return Book</h4>
                    <button type="button" class="btn-close" @click="closeModal"></button>
                </div>
                <div class="modal-body">
                    <div v-if="loading" class="text-center my-3">
                        <span class="spinner-border"></span>
                    </div>
                    <div v-else>
                        <div v-if="alert.show" :class="`alert alert-${alert.type}`" role="alert">
                            {{ alert.text }}
                        </div>
                        <form @submit.prevent="onReturn">
                            <div class="mb-3">
                                <label class="form-label">Select User</label>
                                <select v-model="selectedUserId" class="form-select" required>
                                    <option value="" disabled>Select user</option>
                                    <option v-for="user in users" :key="user.user_id" :value="user.user_id">
                                        {{ user.first_name }} {{ user.last_name }}
                                    </option>
                                </select>
                            </div>
                            <div class="mb-3" v-if="selectedUserBooks.length">
                                <label class="form-label">Select Book to Return</label>
                                <select v-model="selectedBorrowId" class="form-select" required>
                                    <option value="" disabled>Select book</option>
                                    <option v-for="book in selectedUserBooks" :key="book.borrow_id"
                                        :value="book.borrow_id">
                                        {{ book.title }}
                                    </option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-success w-100 mb-2"
                                :disabled="!selectedBorrowId">Confirm Return</button>
                            <button type="button" class="btn btn-secondary w-100" @click="closeModal">Cancel</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
    name: 'ReturnBookForm',
    emits: ['close', 'returned'],
    setup(_, { emit }) {
        const loading = ref(true)
        const alert = ref({ show: false, type: '', text: '' })
        const users = ref([])
        const selectedUserId = ref('')
        const selectedBorrowId = ref('')

        const fetchUsersWithBorrows = async () => {
            loading.value = true
            try {
                const { data } = await axios.get('/api/borrowed-users/')
                users.value = data
            } catch {
                alert.value = { show: true, type: 'danger', text: 'Failed to load users.' }
            } finally {
                loading.value = false
            }
        }

        const selectedUserBooks = computed(() => {
            const user = users.value.find(u => u.user_id === selectedUserId.value)
            return user ? user.books : []
        })

        const onReturn = async () => {
            if (!selectedBorrowId.value) {
                alert.value = { show: true, type: 'danger', text: 'Please select a book.' }
                return
            }
            loading.value = true
            alert.value = { show: false, type: '', text: '' }
            try {
                await axios.post(`/api/return/${selectedBorrowId.value}/`)
                alert.value = { show: true, type: 'success', text: 'Book returned successfully!' }
                setTimeout(() => {
                    emit('returned')
                    closeModal()
                }, 1000)
            } catch (err) {
                let msg = 'Return failed.'
                const resp = err.response?.data
                if (resp?.detail) msg = resp.detail
                alert.value = { show: true, type: 'danger', text: msg }
            } finally {
                loading.value = false
            }
        }

        const closeModal = () => emit('close')

        onMounted(fetchUsersWithBorrows)

        return {
            loading,
            alert,
            users,
            selectedUserId,
            selectedBorrowId,
            selectedUserBooks,
            onReturn,
            closeModal
        }
    }
}
</script>

<style scoped>
.modal {
    display: block;
}
</style>