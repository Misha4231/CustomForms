<script setup lang="ts">
import { createApolloUserClient } from '@/services/graphQL';
import type { ApolloClient, NormalizedCacheObject } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import { ref } from 'vue';

const route = useRoute();

const profile = ref({});

const userClient: ApolloClient<NormalizedCacheObject> = createApolloUserClient();
console.log(route.params.userId);

const fetchProfile = async () => {
    
}

</script>

<template>
    <h1>Profile</h1>
</template>