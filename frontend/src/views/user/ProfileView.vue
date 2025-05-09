<script setup lang="ts">
import { gql } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import router from '@/router';
import { useProfileStore } from '@/stores/auth';
import { useMutation } from '@vue/apollo-composable'
import type { ProfileData } from '@/interfaces/Profile';
import { createApolloClient } from '@/services/graphQL';
import TopSide from '@/components/profile/TopSide.vue';
import FormsList from '@/components/profile/FormsList.vue';

const route = useRoute();
const userIdParam = parseInt(Array.isArray(route.params.userId) ? route.params.userId[0] : route.params.userId);
const currentUserProfile = useProfileStore();

const profile = ref({fullname: '', avatar: ''});
const newProfileData = ref<ProfileData>({fullname: '', avatar: null});

const isEditable = userIdParam == currentUserProfile.id; // number to string

// =================== PAGE CREATION ===============
// method to fetch a profile data
const fetchProfile = async () => {
    const client = createApolloClient();
    try {
        const queryResult = await client.query({
            query: gql`
                    query profileQuery($id: Int) {
                        profile(id: $id) {
                            fullname
                            avatar
                        }
                    }`,
            variables: {
                id: userIdParam
            }
        });

        profile.value = queryResult.data.profile;
        if (userIdParam == currentUserProfile.id) { // i.e. user can change profile info
            newProfileData.value.avatar = profile.value.avatar;
            newProfileData.value.fullname = profile.value.fullname;
        }
    } catch (err) { // if user is not found or other error occured, redirect to 404 page
        router.push({'path': '/404'})
    }
}
onMounted(async () => {
    await fetchProfile();
})

// =================== SUBMIT NEW DATA ===============
const updateUserMutation = gql`
mutation UpdateUser($id: Int!, $fullname: String!, $avatar: Upload!) {
  updateUser(id: $id, fullname: $fullname, avatar: $avatar) {
    user {
      fullname
      avatar
    }
  }
}
`;
const {mutate: updateUser} = useMutation(updateUserMutation);

const updateProfile = async() => {
    try {
        await updateUser({
            id: userIdParam,
            avatar: newProfileData.value.avatar,
            fullname: newProfileData.value.fullname
        });
    } catch(err) {
        return;
    }
}
const handleFileUpdate = (file: File) => {
  newProfileData.value.avatar = file;
};

const handleNameUpdate = (name: string) => {
  newProfileData.value.fullname = name;
};
</script>

<template>
    <h1>Profile</h1>

    <TopSide
        :profile="profile"
        :newProfileData="newProfileData"
        :isEditable="isEditable"
        @update:file="handleFileUpdate"
        @update:name="handleNameUpdate"
    />

    <div class="mt-3" v-if="isEditable">
        <button @click="updateProfile" type="button" class="btn btn-primary mb-5">Save Changes</button>
    </div>

    <h2>Forms:</h2>
    <FormsList
        :userId="userIdParam"
        :isEditable="isEditable"
    />
</template>