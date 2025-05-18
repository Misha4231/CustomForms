<script setup lang="ts">
    import { mediaHost } from '@/services/apiHost';
    import { computed, defineProps, ref, watch } from 'vue';
    import ImageContent from './contentSections/ImageContent.vue';
    import VideoContent from './contentSections/VideoContent.vue';
    import TextContent from './contentSections/TextContent.vue';


    const props = defineProps<{
        data: {
            image: string,
            text: string,
            type: string,
            video: string
        },
        sectionId: string,
        isEditable: boolean
    }>();
    
    const selectedType = ref(props.data.type);
    watch(() => props.data.type, (newVal) => {
        selectedType.value = newVal;
    })

    const selectedTypeComponent = computed(() => {
        switch (selectedType.value) {
            case 'IMAGE': return ImageContent;
            case 'VIDEO': return VideoContent;
            default: return TextContent;
        }
    });
</script>

<template>
    <div class="content-wrapper d-flex justify-content-between">
        <component
            :is="selectedTypeComponent"
            :data="props.data"
            :isEditable="props.isEditable"
            :sectionId="props.sectionId"
        />

        <div class="content-types-select" style="width: 20%;" v-if="isEditable">
            <span>Content Type: </span>
            <select class="form-select" v-model="selectedType">
                <option value="TEXT">Plain text</option>
                <option value="IMAGE">Image</option>
                <option value="VIDEO">Video</option>
            </select>
        </div>
    </div>
</template>
