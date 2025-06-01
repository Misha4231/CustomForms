<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{
  data: { isRequired: boolean },
  sectionId: string,
  isEditable: boolean,
  changeAnswer: (sectionId: number, data: any) => void
}>();
</script>

<template>
    <div class="w-75">
        <textarea class="form-control" :disabled="isEditable" maxlength="1000" @change="(e: Event) => {
          const newVal = (e.target as HTMLInputElement).value;
          
          changeAnswer(parseInt(sectionId), {text: newVal});
          }"></textarea>
    </div>
</template>