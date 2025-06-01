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
    <div class="w-25">
        <input type="date" class="form-control" :disabled="isEditable" @change="(e: Event) => {
          const newVal = (e.target as HTMLTextAreaElement).value;

          changeAnswer(parseInt(sectionId), {date: newVal});
        }">
    </div>
</template>