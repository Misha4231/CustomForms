import { ApolloClient, HttpLink, type NormalizedCacheObject } from "@apollo/client/core";
import { InMemoryCache } from "@apollo/client/core";
import { setContext } from '@apollo/client/link/context';
import { apiHost, getCookie } from "./apiHost";
import createUploadLink from "apollo-upload-client/createUploadLink.mjs";

let apolloUserClient: ApolloClient<NormalizedCacheObject> | null = null;

// create appolo client for graphQL queries
export function createApolloClient() {
    if (apolloUserClient) return apolloUserClient;

    const csrfLink = setContext((_, { headers }) => { // headers with csrf token included for session purpose
        const csrfToken = getCookie('csrftoken');
        return {
            headers: {
                ...headers,
                'X-CSRFToken': csrfToken,
            },
        };
    });

    const httpLink = createUploadLink({
        uri: `${apiHost}graphql/`,
        credentials: 'include',
    });

    return apolloUserClient = new ApolloClient({
        link: csrfLink.concat(httpLink),
        cache: new InMemoryCache(),
    })
}