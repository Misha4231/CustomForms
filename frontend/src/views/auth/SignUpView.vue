<script setup lang="ts">
import { ref, type Ref } from 'vue';
import api from '@/services/RESTapi';
import { AxiosError } from 'axios';
import router from '@/router';

const userInput = ref({ email: '', password1: '', password2: '' });

// error handling refs
const errorMsg: Ref<string> = ref('');
const invalidInputs: Ref<Array<string>> = ref([]);


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
        const response = await api.post('/auth/registration/', JSON.stringify(userInput.value));

        router.push({path: '/sign-in'})
        
    } catch (error) { // error handling
        const err = error as AxiosError<Object>; // specify a type
        if (err.response) {
            const data: Record<string, any> = err.response.data;

            for (const property in data) { // parse all properties
                if (property !== "non_field_errors") { // specific input field
                    invalidInputs.value.push(property)
                }

                for (const msg of data[property]) { // iterate through messages
                    errorMsg.value += msg + '<br>';
                } 
            }
        }
        
    }
    
}
</script>


<template>
    <form class="container col-md-6" @submit="submitHandler">
        <h1 class="text-center mb-4">Sign up</h1>

        <div class="form-floating mb-3">
            <input v-model="userInput.email" type="email" class="form-control" :class="{'is-invalid': invalidInputs.includes('email')}" id="emailInput" placeholder="Email address" required>
            <label for="emailInput">Email address</label>
        </div>
        <div class="form-floating mb-3">
            <input v-model="userInput.password1" type="password" class="form-control" :class="{'is-invalid': invalidInputs.includes('password1')}" id="password1Input" placeholder="Password" required>
            <label for="password1Input">Password</label>
        </div>
        <div class="form-floating mb-2">
            <input v-model="userInput.password2" type="password" class="form-control" :class="{'is-invalid': invalidInputs.includes('password2')}" id="password2Input" placeholder="Confirm Password" required>
            <label for="password2Input">Confirm Password</label>
        </div>

        <p v-if="errorMsg" class="text-danger" v-html="errorMsg"></p> <!--v-html to use line breaks-->

        <div class="text-center mt-3">
            <button type="submit" class="btn btn-primary">Submit</button>
        </div>

        <p class="text-center mt-4">
            Already have an account? <RouterLink to="/sign-in">Sign In</RouterLink>
        </p>
    </form>
</template>