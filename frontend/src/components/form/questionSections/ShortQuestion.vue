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
        <input type="text" class="form-control" :disabled="isEditable">
    </div>
</template>