<script setup lang="ts">
import { mediaHost } from '@/services/apiHost';
import { defineProps, ref, watch } from 'vue';

const props = defineProps<{
  data: { video: string },
  sectionId: string,
  isEditable: boolean,
  updateContent: (sectionId: number, data: any) => void;
}>();

const localVideo = ref<string>(mediaHost + props.data.video);
watch(() => props.data.video, (v) => localVideo.value = mediaHost + v);

function handleUpload(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const file = target.files[0];
    localVideo.value = URL.createObjectURL(file);

    props.updateContent(parseInt(props.sectionId), {
      content: {
        type: 'video',
        video: file
      }
    });

    
  }
}
</script>

<template>
  <div class="content-image-wrapper">
    <div class="video-wrapper">
      <video :src="localVideo" controls height="350"></video>
    </div>
    <div class="mt-3" v-if="isEditable">
      <label class="form-label">Upload new Video</label>
      <input class="form-control" type="file" @change="handleUpload" />
    </div>
  </div>
</template>

