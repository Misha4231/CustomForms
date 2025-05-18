<script setup lang="ts">
import { mediaHost } from '@/services/apiHost';
import { defineProps } from 'vue';

defineProps<{
  data: { image: string },
  sectionId: string,
  isEditable: boolean
}>();

</script>

<template>
  <div class="content-image-wrapper">
    <img class="img-fluid" :src="mediaHost + data.image" />
    <div class="mt-3" v-if="isEditable">
      <label class="form-label">Upload new Image</label>
      <input class="form-control" type="file" />
    </div>
  </div>
</template>
