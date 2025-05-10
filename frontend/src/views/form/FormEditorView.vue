<script setup lang="ts">
import FormHeader from '@/components/form/FormHeader.vue';
import router from '@/router';
import { createApolloClient } from '@/services/graphQL';
import { useProfileStore } from '@/stores/auth';
import { gql } from '@apollo/client/core';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

    const route = useRoute();
    const profile = useProfileStore();

    const isEditable = ref(false);
    
    const formId = parseInt(route.params.formId as string);
    
onMounted(async () => {
    if (route.query.editor == '1') { // user want's to edit form structure
        const client = createApolloClient();
        try {
            const response = await client.query({ // get form's owner id and compare with current user
                query: gql`
                    query getForm($id: Int!) {
                        form(id: $id) {
                            owner {
                                id
                            }
                        }
                    }
                `,
                variables: {
                    id: formId
                }
            });

            const ownerId = response.data.form.owner.id;

            if (profile.id != ownerId) { // random user want's to edit form
                router.push({'path': '/404'});
            } else {
                isEditable.value = true; // form can be edited
            }
        } catch(err) {
            router.push({'path': `/profile/${profile.id}`});
        }
    }
})
</script>

<template>
    <FormHeader
        :isEditable="isEditable"
        :formId="formId"
    />
</template>