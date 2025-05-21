<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import ShortQuestion from './questionSections/ShortQuestion.vue';
import LongQuestion from './questionSections/LongQuestion.vue';
import OptionedQuestion from './questionSections/OptionedQuestion.vue';
import RangeQuestion from './questionSections/RangeQuestion.vue';
import DateQuestion from './questionSections/DateQuestion.vue';

    const props = defineProps<{
        data: {
            answerType: string,
            isRequired: boolean,
            maxRange: number | null,
            minRange: number | null
        },
        sectionId: string,
        isEditable: boolean,
        updateContent: (sectionId: number, data: any) => void;
    }>()
    
    const selectedType = ref(props.data.answerType);
    watch(() => props.data.answerType, (newVal) => {
        selectedType.value = newVal;
    });

    // pass proper component depending on what user choose
    const selectedTypeComponent = computed(() => {
        switch (selectedType.value) {
            case 'SHORT': return ShortQuestion;
            case 'LONG': return LongQuestion;
            case 'RADIO': return OptionedQuestion; // custom props
            case 'CHECKBOX': return OptionedQuestion; // custom props
            case 'RANGE': return RangeQuestion;
            default: return DateQuestion;
        }
    });

    const selectedTypeProps = computed(() => {
        if (['RADIO', 'CHECKBOX'].includes(selectedType.value)) {
            return {
                data: props.data,
                isEditable: props.isEditable,
                sectionId: props.sectionId,
                questionType: selectedType.value, // pass to OptionedQuestion
                updateContent: props.updateContent
            };
        }
        return {
            data: props.data,
            isEditable: props.isEditable,
            sectionId: props.sectionId,
            updateContent: props.updateContent
        };
    });

    function handleTypeChange(event: Event) {
        const t = event.target as HTMLSelectElement;
        
        props.updateContent(parseInt(props.sectionId), {
            question: {
                answerType: t.value as string
            }
        })
    }
</script>

<template>
    <div class="question-wrapper d-flex justify-content-between">
        <component
            :is="selectedTypeComponent"
            v-bind="selectedTypeProps"
        />

        <div class="question-types-select" style="width: 20%;" v-if="isEditable">
            <span>Question Type: </span>
            <select class="form-select" v-model="selectedType" @change="handleTypeChange">
                <option value="SHORT">Short answer</option>
                <option value="LONG">Long answer</option>
                <option value="RADIO">Multiple choice</option>
                <option value="CHECKBOX">Checkboxes</option>
                <option value="RANGE">Linear scale</option>
                <option value="DATE">Date</option>
            </select>
        </div>
    </div>
</template>