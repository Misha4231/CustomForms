<script setup lang="ts">
import FormHeader from '@/components/form/FormHeader.vue';
import SectionsList from '@/components/form/SectionsList.vue';
import router from '@/router';
import { createApolloClient } from '@/services/graphQL';
import { useProfileStore } from '@/stores/auth';
import { useMutation } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { ComponentPublicInstance, onMounted, ref } from 'vue';
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

const {mutate: submitAnswers} = useMutation(gql`
    mutation submitAnswer($form_id: ID, $answers: [AnswerInputType]) {
        submitAnswer (formId: $form_id, answers: $answers) {
            submission {
                id
            }
        }
    }
`)

const sectionListRef = ref<ComponentPublicInstance<{answers: any}>>();
async function handleSubmit() {
    const submittedAnswers = sectionListRef.value?.answers;
    const response = await submitAnswers({
        form_id: formId,
        answers: submittedAnswers
    });

    const submissionId = response?.data.submitAnswer.submission.id;
    router.push({path: '/submission/' + submissionId});
}
</script>

<template>
    <FormHeader
        :isEditable="isEditable"
        :formId="formId"
    />

    <SectionsList
        ref="sectionListRef"
        :isEditable="isEditable"
        :formId="formId"
    />

    <div class="d-flex justify-content-center">
        <button v-if="!isEditable" @click="handleSubmit" class="btn btn-primary mt-4 mb-5 w-25">
            <h3>Submit</h3>
        </button>
    </div>
</template>