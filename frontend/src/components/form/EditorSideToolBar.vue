<script setup lang="ts">
 defineProps<{
    horizontal: boolean
    order: number
    addSection: (type: 'question' | 'text' | 'image' | 'video', order: number) => void;
 }>();
</script>

<template>
  <div class="d-flex bg-secondary p-2 gap-1 rounded-1 m-auto" :class="horizontal ? 'flex-row mt-2' : 'flex-column'" style="width: min-content;">
    <div class="icon-wrapper" title="Add Question" @click="() => addSection('question', order + 1)">
      <img width="35" src="/icons8-add-100.png" alt="add question" />
    </div>
    <div class="icon-wrapper" title="Add Text">
      <img width="35" src="/icons8-text-90.png" alt="add text" @click="() => addSection('text', order + 1)"/>
    </div>
    <div class="icon-wrapper" title="Add Image">
      <img width="35" src="/icons8-image-100.png" alt="add image" @click="() => addSection('image', order + 1)"/>
    </div>
    <div class="icon-wrapper" title="Add Video">
      <img width="35" src="/icons8-video-100.png" alt="add video" @click="() => addSection('video', order + 1)"/>
    </div>
  </div>
</template>

<style scoped>
.icon-wrapper {
  padding: 4px;
  border-radius: 6px;
  transition: background-color 0.2s;
  cursor: pointer;
}

.icon-wrapper:hover {
  background-color: rgba(255, 255, 255, 0.2); 
}
</style>
