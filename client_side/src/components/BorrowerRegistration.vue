<template>
    <div class="container py-5">
        <h3 class="mb-4"><i class="fas fa-users me-2"></i>Borrower Accounts</h3>

        <!-- Borrower List -->
        <div class="table-responsive mb-4">
            <table class="table table-bordered table-striped">
                <thead class="table-success">
                    <tr>
                        <th>#</th>
                        <th>Full Name</th>
                        <th>Username</th>
                        <th>Email</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(borrower, index) in borrowers" :key="borrower.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ borrower.first_name }} {{ borrower.last_name }}</td>
                        <td>{{ borrower.username }}</td>
                        <td>{{ borrower.email }}</td>
                    </tr>
                    <tr v-if="borrowers.length === 0">
                        <td colspan="4" class="text-center text-muted">No borrowers found.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Toggle Form -->
        <button class="btn btn-success mb-4" @click="showForm = !showForm">
            <i class="fas fa-user-plus me-2"></i>{{ showForm ? 'Hide Form' : 'Add New Borrower' }}
        </button>

        <!-- Registration Form -->
        <div v-if="showForm">
            <h4 class="mb-3"><i class="fas fa-user-plus me-2"></i>Create Borrower Account</h4>
            <form @submit.prevent="registerBorrower" class="row g-3">
                <!-- First Name -->
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-id-badge"></i></span>
                        <input type="text" class="form-control" placeholder="First Name" v-model="firstName" required />
                    </div>
                </div>

                <!-- Last Name -->
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-id-badge"></i></span>
                        <input type="text" class="form-control" placeholder="Last Name" v-model="lastName" required />
                    </div>
                </div>

                <!-- Email -->
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                        <input type="email" class="form-control" placeholder="Email" v-model="email" required />
                    </div>
                </div>

                <!-- Username -->
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-user"></i></span>
                        <input type="text" class="form-control" placeholder="Username" v-model="username" required />
                    </div>
                </div>

                <!-- Password -->
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-lock"></i></span>
                        <input type="password" class="form-control" placeholder="Password" v-model="password"
                            required />
                    </div>
                </div>

                <!-- Confirm Password -->
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-lock"></i></span>
                        <input type="password" class="form-control" placeholder="Confirm Password"
                            v-model="confirmPassword" required />
                    </div>
                </div>

                <div class="col-12">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-user-plus me-2"></i>Create Account
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default {
    name: 'BorrowerRegistration',
    setup() {
        const store = useStore();
        const borrowers = ref([]);
        const showForm = ref(false);
        const errorMessage = ref('');


        const firstName = ref('');
        const lastName = ref('');
        const email = ref('');
        const username = ref('');
        const password = ref('');
        const confirmPassword = ref('');

        const fetchBorrowers = async () => {
            try {
                const response = await axios.get('/api/borrowers/');
                borrowers.value = response.data;
            } catch (err) {
                console.error('Failed to fetch borrowers:', err);
            }
        };

        const registerBorrower = async () => {
            if (password.value !== confirmPassword.value) {
                return alert('Passwords do not match.');
            }

            try {
                await store.dispatch('registerBorrowerAsAdmin', {
                    first_name: firstName.value,
                    last_name: lastName.value,
                    email: email.value,
                    username: username.value,
                    password: password.value
                });
                alert('Borrower account successfully created.');

                // Reset form
                firstName.value = lastName.value = email.value = username.value = password.value = confirmPassword.value = '';
                showForm.value = false;
                await fetchBorrowers();
            } catch (err) {
    if (err.response && err.response.data) {
        const data = err.response.data;
        if (data.username) {
        errorMessage.value = data.username[0];
        } else if (data.email) {
        errorMessage.value = data.email[0];
        } else {
        errorMessage.value = 'Failed to create borrower. Please try again.';
        }
    } else {
        errorMessage.value = 'Something went wrong. Please try again.';
    }
    }

        };

        onMounted(fetchBorrowers);

        return {
            borrowers,
            showForm,
            firstName,
            lastName,
            email,
            username,
            password,
            confirmPassword,
            registerBorrower,
            errorMessage 
        };
    }
};
</script>
