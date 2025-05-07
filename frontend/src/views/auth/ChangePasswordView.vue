<script setup lang="ts">
import { ref, type Ref } from 'vue';
import api from '@/services/RESTapi';
import { AxiosError, type AxiosResponse } from 'axios';
import router from '@/router';
import { useProfileStore } from '@/stores/auth';

const userInput = ref({ new_password1: '', new_password2: '' });
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
        await api.post('/auth/password/change/', JSON.stringify(userInput.value));

        router.push({path: `/profile/${profileStore.id}`})
    } catch (error) { // error handling
        const err = error as AxiosError<Object>; // specify a type

        if (err.response) {
            const data: Record<string, any> = err.response.data;     
           
            
            if (data.new_password2)
                errorMsg.value = data.new_password2[0];
        }
        
    }
    
}
</script>


<template>
    <form class="container col-md-6" @submit="submitHandler">
        <h1 class="text-center mb-4">Change password</h1>

        <div class="form-floating mb-3">
            <input v-model="userInput.new_password1" type="password" class="form-control" id="newPassword1Input" placeholder="New Password" required>
            <label for="newPassword1Input">New Password</label>
        </div>
        <div class="form-floating mb-3">
            <input v-model="userInput.new_password2" type="password" class="form-control" id="newPassword2Input" placeholder="New Password 2" required>
            <label for="newPassword2Input">New Password Confirmation</label>
        </div>

        <p v-if="errorMsg" class="text-danger" v-html="errorMsg"></p> <!--v-html to use line breaks-->

        <div class="text-center mt-3">
            <button type="submit" class="btn btn-primary">Submit</button>
        </div>
    </form>
</template>