<script setup lang="ts">
import { createApolloClient } from '@/services/graphQL';
import { useMutation } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { onMounted, reactive, ref } from 'vue';

const props = defineProps<{
    isEditable: boolean,
    formId: number
}>();

const form = reactive<{
    title: string,
    description: string
}>({title: '', description: ''});

const {mutate: updateForm} = useMutation(gql`
    mutation updateForm($id: ID, $title: String, $description: String){
        updateForm(id: $id, title: $title, description: $description) {
            form {
                id
            }
        }
    }
`)
// mutate data on title change
const titleChagned = async(event: Event) => {
    const target = event.target as HTMLInputElement;
    form.title = target.value;

    await updateForm({
        id: props.formId,
        title: form.title
    });
}
// mutate data on description change
const descriptionChagned = async(event: Event) => {
    const target = event.target as HTMLInputElement;
    form.description = target.value;

    await updateForm({
        id: props.formId,
        description: form.description
    });
}

onMounted(async() => {
    const client = createApolloClient();
    const response = await client.query({
        query: gql`
            query getForm($id: Int!) {
                form(id: $id) {
                    title
                    description
                }
            }`,
        variables: {
            id: props.formId
        }
    });

    form.title = response.data.form.title;
    form.description = response.data.form.description;
});

// get link without GET param
const shareLink = window.location.href.split("?")[0];
</script>

<template>
    <div class="container d-flex justify-content-center">
        <div class="w-100" style="max-width: 900px;">
            <div class="rounded bg-secondary p-4 shadow">
                <div class="d-flex align-items-center gap-2">
                    <input v-if="isEditable" @change="titleChagned" :value="form.title" type="text" class="form-control form-control-lg bg-dark text-light border-0 mb-3" placeholder="Form title">
                    <h1 class="mb-3" v-else>{{ form.title }}</h1>

                    <button v-if="isEditable" class="btn btn-success mb-3" type="button" data-bs-toggle="modal" data-bs-target="#shareModal">
                        <img height="35" src="/icons8-share-90.png" alt="Share form">
                    </button>
                </div>

                <textarea v-if="isEditable" @change="descriptionChagned" :value="form.description" class="form-control bg-dark text-light border-0" rows="5" placeholder="Form description"></textarea>
                <p v-else>{{ form.description }}</p>
            </div>
        </div>
    </div>


    <div class="modal fade" id="shareModal" tabindex="-1" aria-labelledby="shareModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="shareModalLabel">Share this form</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <a :href="shareLink">{{ shareLink }}</a> 
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>
            </div>
            </div>
        </div>
    </div>
</template>