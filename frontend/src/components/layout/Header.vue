<script setup>
import { useProfileStore } from '@/stores/auth';
import { computed } from 'vue';

const profileStore = useProfileStore();

const signedIn = computed(() => profileStore.id !== null);
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-md navbar">
            <div class="container-fluid">
                <RouterLink class="navbar-brand fs-2" to="/">Custom Forms</RouterLink>

                <div class="d-flex">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item dropdown" v-if="signedIn">
                            <div class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <img :src="profileStore.avatar === null ? '/user.png' : profileStore.avatar" class="rounded-circle" width="30" height="30" alt="avatar">
                            </div>
                            <ul class="dropdown-menu">
                                <li><RouterLink :to="'/profile/' + profileStore.id" class="dropdown-item">My Profile</RouterLink></li>
                                <li><RouterLink to="/change-password" class="dropdown-item">Change Password</RouterLink></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><RouterLink to="/logout" class="dropdown-item">Logout</RouterLink></li>
                            </ul>
                        </li>
                        <template v-else>
                            <li class="nav-item">
                                <RouterLink class="nav-link" to="/sign-in">Sign In</RouterLink>
                            </li>
                            <li class="nav-item">
                                <RouterLink class="nav-link" to="/sign-up">Sign Up</RouterLink>
                            </li>
                        </template>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</template>