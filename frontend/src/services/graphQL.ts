import { ApolloClient, HttpLink, type NormalizedCacheObject } from "@apollo/client/core";
import { InMemoryCache } from "@apollo/client/core";
import { setContext } from '@apollo/client/link/context';
import { apiHost } from "./apiHost";

let apolloUserClient: ApolloClient<NormalizedCacheObject> | null = null;

// create appolo client for graphQL queries
export function createApolloUserClient() {
    if (apolloUserClient) return apolloUserClient;

    // get cookie (used to search for csrf)
    function getCookie(name: string) {
        let res = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    res = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return res;
    }

    const csrfLink = setContext((_, { headers }) => { // headers with csrf token included for session purpose
        const csrfToken = getCookie('csrftoken');
        return {
            headers: {
                ...headers,
                'X-CSRFToken': csrfToken,
            },
        };
    });

    const httpLink = new HttpLink({
        uri: `${apiHost}users/graphql/`,
        credentials: 'include',
    });

    return apolloUserClient = new ApolloClient({
        link: csrfLink.concat(httpLink),
        cache: new InMemoryCache(),
    })
}