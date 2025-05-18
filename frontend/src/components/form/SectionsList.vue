<script setup lang="ts">
import { createApolloClient } from '@/services/graphQL';
import { gql } from '@apollo/client/core';
import { onMounted, reactive } from 'vue';
import SectionQuestion from './SectionQuestion.vue';
import SectionContent from './SectionContent.vue';

const props = defineProps<{
    formId: number,
    isEditable: boolean
}>();

let sections = reactive<any[]>([]);
onMounted(async() => {
    const client = createApolloClient();
    const response = await client.query({
        query: gql`
            query section($formId: ID!) {
            sectionsByForm(formId: $formId){
                id
                title

                item {
                    __typename
                    ... on ContentType {
                        type
                        text
                        image
                        video
                    }
                    __typename
                    ... on QuestionType {
                        answerType
                        isRequired
                        minRange
                        maxRange
                    }
                }
            }
            }
        `,
        variables: {
            formId: props.formId
        }
    });
    
    sections.splice(0, sections.length, ...response.data.sectionsByForm);
});

</script>

<template>
    <div class="container d-flex flex-column justify-content-center">
        <div class="w-100 mt-2" style="max-width: 900px;margin: auto;" v-for="section in sections" :key="section.id">
            <div class="rounded bg-secondary p-4 shadow">
                <input v-if="isEditable" type="text" class="form-control form-control-medium bg-dark text-light border-0 mb-3" :placeholder="section.item.__typename == 'ContentType' ? 'Section title' : 'Question'">
                <h3 v-else>{{ section.title }} <span v-if="section.item.__typename == 'QuestionType' && section.item.isRequired">*</span></h3>
                
                <SectionContent v-if="section.item.__typename == 'ContentType'"
                    :data="section.item"
                    :sectionId="section.id"
                    :isEditable="isEditable"
                />
                <SectionQuestion v-else
                    :data="section.item"
                    :sectionId="section.id"
                    :isEditable="isEditable"
                />
            </div>
        </div>
    </div>
</template>