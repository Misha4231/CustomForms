import axios from "axios";
import { apiHost, getCookie } from "./apiHost";

// reusable axios configuration
const api = axios.create({
    baseURL: apiHost,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    }
})

export default api;