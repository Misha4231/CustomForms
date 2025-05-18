<script setup lang="ts">
import { ref, watch } from 'vue';

    const props = defineProps<{
        data: {
            answerType: string,
            isRequired: boolean,
            maxRange: number | null,
            minRange: number | null
        },
        sectionId: string,
        isEditable: boolean
    }>()
    
    const selectedType = ref(props.data.answerType);
    watch(() => props.data.answerType, (newVal) => {
        selectedType.value = newVal;
    });
</script>

<template>
    <div class="question-wrapper d-flex justify-content-between">
        <div class="question-types-select" style="width: 20%;" v-if="isEditable">
            <span>Question Type: </span>
            <select class="form-select" v-model="selectedType">
                <option value="SHORT">Short answer</option>
                <option value="LONG">Long answer</option>
                <option value="RADIO">Multiple choice</option>
                <option value="CHECKBOX">Checkboxes</option>
                <option value="DROPDOWN">Dropdown</option>
                <option value="RANGE">Linear scale</option>
                <option value="DATE">Date</option>
            </select>
        </div>
    </div>
</template>