import { createApolloClient } from '@/services/graphQL';
import { gql, type ApolloClient, type NormalizedCacheObject } from '@apollo/client/core';
import { DefaultApolloClient } from '@vue/apollo-composable';
import { defineStore } from 'pinia'

export const useProfileStore = defineStore('profile', {
    state: () => ({
        id: null as number | null,
        avatar: null as string | null
    }),
    actions: {
        setData(id: number | null, avatar: string | null) {
            this.id = id;
            if (avatar === '')
                this.avatar = null;
            else
                this.avatar = avatar;
        },
        async loadUser() { // load user data (must be called before other actions)
            //const client: ApolloClient<NormalizedCacheObject> = createApolloUserClient();
            const client = createApolloClient();

            try {
                const queryResult = await client.query({ // make an graphQL query to get currnet user based on cookies
                    query: gql`
                    query {
                        me {
                            id
                            avatar
                        }
                    }`
                });
                
                this.setData(queryResult.data.me.id, queryResult.data.me.avatar);
            } catch (error) {
                this.setData(null, null);
            }
        }
    }
})