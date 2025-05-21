<script setup lang="ts">
import { mediaHost } from '@/services/apiHost';
import { defineProps, ref, watch } from 'vue';

const props = defineProps<{
  data: { image: string },
  sectionId: string,
  isEditable: boolean,
  updateContent: (sectionId: number, data: any) => void;
}>();

const localImage = ref<string>(mediaHost + props.data.image);
watch(() => props.data.image, (v) => localImage.value = mediaHost + v);

function handleUpload(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const file = target.files[0];
    localImage.value = URL.createObjectURL(file);

    props.updateContent(parseInt(props.sectionId), {
      content: {
        type: 'image',
        image: file
      }
    });

    
  }
}
</script>

<template>
  <div class="content-image-wrapper">
    <img class="img-fluid" :src="localImage" />
    <div class="mt-3" v-if="isEditable">
      <label class="form-label">Upload new Image</label>
      <input class="form-control" type="file" @change="handleUpload" />
    </div>
  </div>
</template>
