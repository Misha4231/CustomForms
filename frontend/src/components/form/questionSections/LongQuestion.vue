<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{
  data: { isRequired: boolean },
  sectionId: string,
  isEditable: boolean
}>();
</script>

<template>
    <div class="w-75">
        <textarea class="form-control" :disabled="isEditable"></textarea>
    </div>
</template>