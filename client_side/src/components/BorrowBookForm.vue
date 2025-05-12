<template>
    <div class="modal fade show d-block" tabindex="-1" style="background:rgba(0,0,0,0.5);">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">Borrow Book</h4>
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
                        <div v-if="book">
                            <h5>{{ book.title }}</h5>
                            <p class="mb-1"><strong>Author:</strong> {{ book.author }}</p>
                            <p class="mb-1"><strong>Available Copies:</strong> {{ book.copies_available }}</p>
                            <p class="mb-3"><strong>ISBN:</strong> {{ book.isbn }}</p>
                        </div>
                        <form @submit.prevent="onBorrow">
                            <div class="mb-3">
                                <label for="userSelect" class="form-label">Select Borrower</label>
                                <select id="userSelect" v-model="selectedUser" class="form-select" required>
                                    <option value="" disabled>Select user</option>
                                    <option v-for="user in users" :key="user.id" :value="user.id">
                                        {{ user.first_name }} {{ user.last_name }} ({{ user.username }})
                                    </option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-success w-100 mb-2">Confirm Borrow</button>
                            <button type="button" class="btn btn-secondary w-100" @click="closeModal">Cancel</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'

export default {
    name: 'BorrowBookForm',
    props: {
        show: { type: Boolean, default: false },
        book: { type: Object, required: true }
    },
    emits: ['close', 'borrowed'],
    setup(props, { emit }) {
        const loading = ref(true)
        const alert = ref({ show: false, type: '', text: '' })
        const users = ref([])
        const selectedUser = ref('')

        // Fetch users (borrowers)
        const fetchData = async () => {
            loading.value = true
            try {
                const usersRes = await axios.get('/api/borrowers/')
                users.value = usersRes.data
            } catch {
                alert.value = { show: true, type: 'danger', text: 'Failed to load users.' }
            } finally {
                loading.value = false
            }
        }

        const onBorrow = async () => {
            if (!selectedUser.value) {
                alert.value = { show: true, type: 'danger', text: 'Please select a user.' }
                return
            }
            loading.value = true
            alert.value = { show: false, type: '', text: '' }
            try {
                await axios.post('/api/borrow/', { book_id: props.book.id, user_id: selectedUser.value })
                alert.value = { show: true, type: 'success', text: 'Book borrowed successfully!' }
                setTimeout(() => {
                    emit('borrowed')
                    closeModal()
                }, 1000)
            } catch (err) {
                let msg = 'Borrow failed.'
                const resp = err.response?.data
                if (resp?.non_field_errors?.length) {
                    msg = resp.non_field_errors[0]
                } else if (resp?.detail) {
                    msg = resp.detail
                }
                alert.value = { show: true, type: 'danger', text: msg }
            } finally {
                loading.value = false
            }
        }

        const closeModal = () => {
            emit('close')
        }

        // Optional: close modal on ESC key
        const handleEsc = (e) => {
            if (e.key === 'Escape') closeModal()
        }
        onMounted(() => {
            fetchData()
            window.addEventListener('keydown', handleEsc)
        })
        watch(() => props.show, (val) => {
            if (!val) window.removeEventListener('keydown', handleEsc)
        })

        return {
            loading,
            alert,
            book: props.book,
            users,
            selectedUser,
            onBorrow,
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