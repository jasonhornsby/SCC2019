import axios, { AxiosResponse } from 'axios';
import router from '@/router';

const authServiceURL = "https://nanyte.design/api/auth";

async function register(username: string, password: string) {
    let response: AxiosResponse;
    try {
        response = await axios.post(authServiceURL + '/register', { username, password });
    } catch (e) {
        if (e.response.status === 409) {
            throw new Error('Username already exists');
        }
        return;
    }
    return response.data;
}

async function login(username: string, password: string) {
    let response: AxiosResponse;
    try {
        response = await axios.post(authServiceURL + '/login', { username, password });
    } catch (e) {
        if (e.response.status === 401) {
            throw new Error('Wrong username or password');
        }
        return;
    }
    return response.data;
}

async function getUsers() {
    let response: AxiosResponse;
    try {
        response = await axios.get('https://nanyte.design/users');
    } catch (e) {
        console.error(e);
        return
    }
    return response.data;
}

/**
 * Logout by deleting the token
 */
function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    router.push('/login');
}

async function getAll() {
    const users = await axios.get('https://nanyte.design/users');
    return users.data;
}

/**
 * Save Login token for Later and set all http calls to use it
 * @param token
 */
function setLoginToken(token: string) {
    localStorage.setItem('token', token);
    setAuthHeader(token);
}

function setAuthHeader(token: string) {
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
}



export const userService = {
    login,
    setLoginToken,
    register,
    logout,
    setAuthHeader,
    getAll
};
