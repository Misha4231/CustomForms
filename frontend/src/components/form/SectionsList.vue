<script setup lang="ts">
import { createApolloClient } from '@/services/graphQL';
import { gql } from '@apollo/client/core';
import { onMounted, reactive, ref } from 'vue';
import SectionQuestion from './SectionQuestion.vue';
import SectionContent from './SectionContent.vue';
import EditorSideToolBar from './EditorSideToolBar.vue';
import { useMutation } from '@vue/apollo-composable';

const props = defineProps<{
    formId: number,
    isEditable: boolean
}>();

let sections = reactive<any[]>([]);

// =============== GET SECTIONS
onMounted(async() => {
    const client = createApolloClient();
    const response = await client.query({
        query: gql`
            query section($formId: ID!) {
            sectionsByForm(formId: $formId){
                id
                title
                order
                
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
    
    // make clone to avoid apollo client lock
    const clonedSections = JSON.parse(JSON.stringify(response.data.sectionsByForm));
    sections.splice(0, sections.length, ...clonedSections);
    
    if (sections.length > 0) selectedSectionId.value = sections[0].id;
});

// ============ ADD SECTION
const {mutate: addSection} = useMutation(gql`
        mutation addSection($form_id: ID, $type: String, $order: Int) {
            addSection(formId: $form_id, type: $type, order: $order) {
                section {
                id
                order
                
                    item {
                    __typename
                    ... on ContentType {
                    type
                    }
                    __typename
                    ... on QuestionType {
                    answerType
                    }
                }
                }
            }
        }
    `);
async function handleAddSection(type: 'question' | 'text' | 'image' | 'video', order: number) {
    const response = await addSection({
        form_id: props.formId,
        type: type,
        order: order
    });
    
    const newSection = response?.data.addSection.section;
    sections.splice(newSection.order, 0, newSection);
    selectedSectionId.value = newSection.id;
}

// =========== REMOVE SECTION
const {mutate: removeSection} = useMutation(gql`
    mutation removeSection($section_id: ID) {
        removeSection (sectionId: $section_id) {
            ok
        }
    }
`);
async function handleRemoveSection(id: number) {
    const response = await removeSection({
        section_id: id
    });

    const success = response?.data.removeSection.ok;
    if (success) { // delete section from array
        const filteredSections = sections 
            .filter((s) => s.id != id) // remove deleted section
            .map((s, index) => ({ // reassign order
                ...s,
                order: index
            }));
            
        sections.splice(0, sections.length, ...filteredSections);
    }
}

// ========== SELECTION MANAGEMENT
const selectedSectionId = ref();
function handleSectionClick(id: string) {
    selectedSectionId.value = id;
}

// ========== CONTENT UPDATE
const {mutate: updateSection} = useMutation(gql`
        mutation updateSection($section_id: ID!, $title: String, $content: ContentInputType, $question: QuestionInputType) {
            updateSection(sectionId: $section_id, title: $title, content: $content, question: $question) {
                section {
                    title
                }
            }
        }
    `);

async function handleContentUpdate(sectionId: number, data: object) {    
    const response = await updateSection({
        section_id: sectionId,
        ...data
    });
}

</script>

<template>
    <div class="container d-flex flex-column justify-content-center">
        <EditorSideToolBar v-if="sections.length == 0 && isEditable" :horizontal="true" :order="-1" :addSection="handleAddSection"></EditorSideToolBar>

        <div class="w-100 mt-2" style="max-width: 900px;margin: auto;" v-for="section in sections" :key="section.id">
            <div class="position-relative" style="cursor: pointer;" @click="() => handleSectionClick(section.id)">
                <div class="position-absolute" style="top: 0; right: -70px; z-index: 10;" v-if="selectedSectionId == section.id && isEditable">
                    <EditorSideToolBar :horizontal="false" :order="parseInt(section.order)" :addSection="handleAddSection"></EditorSideToolBar>
                </div>

                <div class="rounded bg-secondary p-4 shadow">
                    <input v-model="section.title" @change="(e) => handleContentUpdate(section.id, {title: (e.target as HTMLInputElement).value})" v-if="isEditable" type="text" class="form-control form-control-medium bg-dark text-light border-0 mb-3" :placeholder="section.item.__typename == 'ContentType' ? 'Section title' : 'Question'">
                    <h3 v-else>{{ section.title }} <span v-if="section.item.__typename == 'QuestionType' && section.item.isRequired">*</span></h3>
                    
                    <SectionContent v-if="section.item.__typename == 'ContentType'"
                        :data="section.item"
                        :sectionId="section.id"
                        :isEditable="isEditable"
                        :updateContent="handleContentUpdate"
                    />
                    <SectionQuestion v-else
                        :data="section.item"
                        :sectionId="section.id"
                        :isEditable="isEditable"
                        :updateContent="handleContentUpdate"
                    />

                    <div class="remove-section d-flex justify-content-end" v-if="selectedSectionId == section.id && isEditable">
                        <button type="button" class="btn btn-danger mt-1" @click="() => handleRemoveSection(parseInt(section.id))">
                            Remove Section
                            <img src="/icons8-delete-48.png" width="20" alt="-">
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>