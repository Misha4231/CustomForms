<script setup lang="ts">
import { createApolloClient } from '@/services/graphQL';
import { gql } from '@apollo/client/core';
import { onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const formId = parseInt(route.params.formId as string);

const submissions = reactive<{
    id: number,
    user: {fullname: string},
    submittedAt: string
}[]>([]);

onMounted(async() => {
    const client = createApolloClient();
    const response = await client.query({
        query: gql`
            query getSubmissions($form_id: ID!) {
                getSubmitions(formId: $form_id) {
                    id
                    submittedAt
                    user {
                        fullname
                    }
                }
            }
        `,
        variables: {
            form_id: formId
        }
    });

    submissions.push(...response.data.getSubmitions);
})
</script>

<template>
    <div class="list-group">
        
        <RouterLink v-for="subm in submissions" :to="{path: '/submission/' + subm.id}" class="list-group-item list-group-item-action flex-column align-items-start mb-2" >
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">{{ subm.user ? subm.user.fullname : 'Anonymous' }}</h5>
                <small>{{ subm.submittedAt }}</small>
            </div>
        </RouterLink>
    </div>
</template>

<style scoped>
.list-group-item:hover {
  background-color: #0d6efd; 
  color: white;
}
</style>