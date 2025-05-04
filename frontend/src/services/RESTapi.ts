import axios from "axios";
import { apiHost } from "./apiHost";

// reusable axios configuration
const api = axios.create({
    baseURL: apiHost,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    }
})

export default api;