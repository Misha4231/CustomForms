<script setup lang="ts">
import { mediaHost } from '@/services/apiHost';
import { defineProps } from 'vue';
import { VideoPlayer } from '@videojs-player/vue';
import 'video.js/dist/video-js.css';

defineProps<{
  data: { video: string },
  sectionId: string,
  isEditable: boolean
}>();

</script>

<template>
  <div class="content-image-wrapper">
    <div class="video-wrapper">
      <video-player
        :src="mediaHost + data.video"
        controls
        :height="350"
      />
    </div>
    <div class="mt-3" v-if="isEditable">
      <label class="form-label">Upload new Video</label>
      <input class="form-control" type="file" />
    </div>
  </div>
</template>

