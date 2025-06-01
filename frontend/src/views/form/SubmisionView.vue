<script setup lang="ts">
import { gql } from '@apollo/client/core';
import { reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { createApolloClient } from '@/services/graphQL';

const route = useRoute();
const submissionId = parseInt(route.params.submissionId as string);

const answers = reactive<{
    id: number,
    question: {section: {title: string}, answerType: string},
    shortText: string,
    longText: string,
    selectedOptions: {text: string}[],
    rangeValue: number,
    dateValue: string
}[]>([]);
onMounted(async() => {
    const client = createApolloClient();
    const response = await client.query({
        query: gql`
            query answers($submission_id: ID!) {
                answers(submissionId: $submission_id) {
                    id
                    question {
                        section {
                            title
                        }
                        answerType
                    }
                    shortText
                    longText
                    selectedOptions {
                        text
                    }
                    rangeValue
                    dateValue
                }
            }
        `,
        variables: {
            submission_id: submissionId
        }
    });

    answers.push(...response.data.answers);
})
</script>

<template>
    <div class="list-group">
        <a v-for="answer in answers" href="#" class="list-group-item list-group-item-action flex-column align-items-start">
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">{{ answer.question.section.title }}</h5>
            </div>
            
            <p v-if="answer.question.answerType == 'SHORT'" class="mb-1">{{ answer.shortText }}</p>
            <p v-else-if="answer.question.answerType == 'LONG'" class="mb-1">{{ answer.longText }}</p>
            <ul v-else-if="answer.question.answerType == 'RADIO' || answer.question.answerType == 'CHECKBOX'">
                <li v-for="o in answer.selectedOptions">{{ o.text }}</li>
            </ul>
            <p v-else-if="answer.question.answerType == 'RANGE'" class="mb-1">{{ answer.rangeValue }}</p>
            <p v-else-if="answer.question.answerType == 'DATE'" class="mb-1">{{ answer.dateValue }}</p>
        </a>
    </div>
</template>
