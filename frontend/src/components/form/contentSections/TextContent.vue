<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{
  data: { text: string },
  sectionId: string,
  isEditable: boolean
}>();

</script>

<template>
  <div class="content-text-wrapper w-75">
    <p v-if="!isEditable">{{ data.text }}</p>
    <textarea v-else class="form-control" v-model="data.text"></textarea> 
  </div>
</template>
