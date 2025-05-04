<script setup>
import api from '@/services/RESTapi';
import { useProfileStore } from '@/stores/auth';
import { onMounted } from 'vue';

const profileStorate = useProfileStore();

const logout = async () => {
    const response = await api.post("/auth/logout/");

    profileStorate.setData(null, null);
}

onMounted(() => {
    logout();
})
</script>

<template>
    <p>You have successfully logged out. <RouterLink to="/sign-in">Sign in</RouterLink></p>
</template>