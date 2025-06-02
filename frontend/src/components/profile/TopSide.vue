<script setup lang="ts">
import { ref, watch } from 'vue';
import { mediaHost } from '@/services/apiHost';
import type { ProfileData } from '@/interfaces/Profile';

const props = defineProps<{
    profile: ProfileData,
    newProfileData: ProfileData,
    isEditable: boolean,
}>();

const emit = defineEmits<{
    (e: 'update:file', file: File): void;
    (e: 'update:name', name: string): void;
}>();
const handleFileChange = (event: Event) => { // called when input file get new data
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        emit('update:file', target.files[0]);
    }
};
const updateName = (event: Event) => {
    const target = event.target as HTMLInputElement;
    emit('update:name', target.value);
};
</script>

<template>
    <div class="mt-5 nav">
        <div class="mr-2 flex-column justify-content-center" style="width: 300px;">
            <img :src="profile.avatar ? ((profile.avatar as string).startsWith('blob') ? profile.avatar : mediaHost + profile.avatar) : '/user.png'"  class="rounded-circle" width="100" height="100" alt="avatar">
            <div class="mt-2" v-if="isEditable">
                <label for="formFile" class="form-label">Choose new avatar</label>
                <input type="file" id="formFile" class="form-control" accept=".png,.jpg,.jpeg" @change="handleFileChange">
            </div>
        </div>
        <div class="form-floating" v-if="isEditable" style="width: 400px;">
            <input type="text" class="form-control" id="floatingFullNameInput" placeholder="full name" :value="newProfileData.fullname" @input="updateName">
            <label for="floatingFullNameInput">Full name</label>
        </div>
        <div v-else>
            <h3>{{ profile.fullname }}</h3>
        </div>
    </div>
</template>