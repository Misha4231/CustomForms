<script setup lang="ts">
import { defineProps, ref, watch } from 'vue';

const props = defineProps<{
  data: { 
    isRequired: boolean,
    maxRange: number,
    minRange: number
   },
  sectionId: string,
  isEditable: boolean,
  updateContent: (sectionId: number, data: any) => void,
  changeAnswer: (sectionId: number, data: any) => void
}>();

const range = ref<{maxRange: number, minRange: number}>({maxRange: props.data.maxRange, minRange: props.data.minRange});
watch(() => props.data.maxRange, (v) => range.value.maxRange = v);
watch(() => props.data.minRange, (v) => range.value.minRange = v);

function handleChange() {
  props.updateContent(parseInt(props.sectionId), {
    question: {
      answerType: "RANGE",
      ...range.value
    }
  });
}
</script>

<template>
    <div class="w-75">
        <input :min="data.minRange" :max="data.maxRange" type="range" class="form-range" :disabled="isEditable" @change="(e: Event) => {
          const newVal = parseInt((e.target as HTMLTextAreaElement).value);
          
          changeAnswer(parseInt(sectionId), {rangeVal: newVal});
        }">
        <div class="d-flex justify-content-between" v-if="isEditable">
          <input type="number" class="form-control" style="width: 15%;" v-model="range.minRange" @change="handleChange">
          <input type="number" class="form-control" style="width: 15%;" v-model="range.maxRange" @change="handleChange">
        </div>
        <div class="d-flex justify-content-between" v-else>
          <span>{{ data.minRange }}</span>
          <span>to</span>
          <span>{{ data.maxRange }}</span>
        </div>
    </div>
</template>