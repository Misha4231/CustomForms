<script setup lang="ts">
import { defineProps, ref, watch } from 'vue';

const props = defineProps<{
  data: { text: string },
  sectionId: string,
  isEditable: boolean,
  updateContent: (sectionId: number, data: any) => void;
}>();

const localText = ref(props.data.text);
watch(() => props.data.text, (newText) => {
  localText.value = newText;
});
</script>

<template>
  <div class="content-text-wrapper w-75">
    <p v-if="!isEditable">{{ localText }}</p>
    <textarea v-else class="form-control" @change="() => props.updateContent(parseInt(props.sectionId), { content: {
      type: 'text',
      text: localText
    } })" v-model="localText"></textarea> 
  </div>
</template>
