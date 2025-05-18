<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{
  data: { 
    isRequired: boolean,
    maxRange: number,
    minRange: number
   },
  sectionId: string,
  isEditable: boolean
}>();
</script>

<template>
    <div class="w-75">
        <input :min="data.minRange" :max="data.maxRange" type="range" class="form-range" :disabled="isEditable">
        <div class="d-flex justify-content-between" v-if="isEditable">
          <input type="number" class="form-control" style="width: 15%;" v-model="data.minRange">
          <input type="number" class="form-control" style="width: 15%;" v-model="data.maxRange">
        </div>
        <div class="d-flex justify-content-between" v-else>
          <span>{{ data.minRange }}</span>
          <span>to</span>
          <span>{{ data.maxRange }}</span>
        </div>
    </div>
</template>