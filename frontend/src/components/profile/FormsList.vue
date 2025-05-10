<script setup lang="ts">
import { createApolloClient } from '@/services/graphQL';
import { useMutation } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core';
import { nextTick, onMounted, ref } from 'vue';
import router from '@/router';

const props = defineProps<{
    userId: number
}>();

const forms = ref<{id: number, title: string, description: string}[]>([])
const fetchForms = async() => {
    const client = createApolloClient();
    
    const response = await client.query({
        query: gql`
            query getAllForms($userId: Int!) {
                allUserForms(userId: $userId) {
                    id
                    title
                    description
                }
            }
        `,
        variables: {
            userId: props.userId
        }
    });
    
    forms.value = response.data.allUserForms;
}
onMounted(async () => {
    await fetchForms();
})

const {mutate: formCreateMutation} = useMutation(gql`
mutation CreateForm($title: String!, $description: String){
  createForm(title: $title, description: $description) {
    form {
      id
      title
      description
    }
  }
}
`)
const addForm = async() => {
    const fetch = async() => {
        const result = await formCreateMutation({
            title: "",
            description: ""
        });

        const createdForm = result?.data.createForm.form;
        forms.value = [createdForm, ...forms.value];

        return createdForm.id;
    }
    
    const id = await fetch(); // Wait for DOM to reflect the change
    setTimeout(() => {
        router.push({path: '/form/' + id, query: {editor: 1}});
    }, 100);
}
</script>

<template>
    <div class="d-flex flex-row flex-wrap gap-3">
        <div v-for="form in forms" :key="'form.id'" class="card" style="width: 10rem;">
            <div class="card-body">
                <h5 class="card-title">{{ form.title ? form.title : "No title" }}</h5>
                <p class="card-text">{{ form.description }}</p>
                <RouterLink :to="{path: '/form/' + form.id, query: {editor: 1}}" class="btn btn-primary">Edit -></RouterLink>
            </div>
        </div>
        <div @click="addForm" class="card" style="width: min-content;height: min-content;cursor: pointer;text-decoration: none;">
            <div class="card-body">
                <h1 style="padding: 1rem;font-size: 3rem;">+</h1>
            </div>
        </div>
    </div>
</template>