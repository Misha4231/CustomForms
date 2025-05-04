<script setup lang="ts">
import { ref, type Ref } from 'vue';
import api from '@/services/RESTapi';
import { AxiosError, type AxiosResponse } from 'axios';
import router from '@/router';
import { useProfileStore } from '@/stores/auth';

const userInput = ref({ email: '', password: '' });
const profileStore = useProfileStore();

// error handling refs
const errorMsg: Ref<string> = ref('');

// when Submit button is pressed
const submitHandler = async (event: Event) => {
    const form = event.target as HTMLFormElement;

    if (!form.checkValidity()) { // first validation before backend refering
        errorMsg.value = 'Fill all fields and check data formatting';
        return;
    }

    event.preventDefault();
    try { // try to fetch
        errorMsg.value = '';
        const response = await api.post('/auth/login/', JSON.stringify(userInput.value));
        const data: Record<string, any> = response.data;

        if (data.user)
            profileStore.setData(data.user.pk, null);
        router.push({path: '/profile'})
    } catch (error) { // error handling
        const err = error as AxiosError<Object>; // specify a type
        if (err.response) {
            const data: Record<string, any> = err.response.data;

            if (data.non_field_errors)
                errorMsg.value = data.non_field_errors[0];
        }
        
    }
    
}
</script>


<template>
    <form class="container col-md-6" @submit="submitHandler">
        <h1 class="text-center mb-4">Sign in</h1>

        <div class="form-floating mb-3">
            <input v-model="userInput.email" type="email" class="form-control" id="emailInput" placeholder="Email address" required>
            <label for="emailInput">Email address</label>
        </div>
        <div class="form-floating mb-3">
            <input v-model="userInput.password" type="password" class="form-control" id="passwordInput" placeholder="Password" required>
            <label for="passwordInput">Password</label>
        </div>

        <p v-if="errorMsg" class="text-danger" v-html="errorMsg"></p> <!--v-html to use line breaks-->

        <div class="text-center mt-3">
            <button type="submit" class="btn btn-primary">Submit</button>
        </div>

        <p class="text-center mt-4">
            Don't have an account? <RouterLink to="/sign-up">Sign Up</RouterLink>
        </p>
    </form>
</template>