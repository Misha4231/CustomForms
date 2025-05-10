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
</script>

<template>
    <div class="container d-flex justify-content-center">
        <div class="w-100" style="max-width: 600px;">
            <div class="rounded bg-secondary p-4 shadow">
                <input @change="titleChagned" :value="form.title" type="text" class="form-control form-control-lg bg-dark text-light border-0 mb-3" placeholder="Form title">
                <textarea @change="descriptionChagned" :value="form.description" class="form-control bg-dark text-light border-0" rows="5" placeholder="Form description"></textarea>
            </div>
        </div>
    </div>
</template>