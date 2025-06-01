<script setup lang="ts">
import router from '@/router';
import { useProfileStore } from '@/stores/auth';

const profileStore = useProfileStore();

if (profileStore.id === null) {
    router.push('/sign-in');
} else {
    router.push(`/profile/${profileStore.id}`);
}

</script>


<template>
    <h1>Loading...</h1>
</template>