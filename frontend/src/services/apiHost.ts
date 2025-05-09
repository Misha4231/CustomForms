export function getCookie(name: string) { // get cookie (used to search for csrf)
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

export const apiHost: string = 'http://localhost:8000/';
export const mediaHost: string = apiHost + 'media/';