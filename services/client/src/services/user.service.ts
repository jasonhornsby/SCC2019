import axios, { AxiosResponse } from 'axios';
import router from '@/router';


async function register(username: string, password: string) {
    let response: AxiosResponse;
    try {
        response = await axios.post('http://localhost:8000/register', { username, password });
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
        response = await axios.post('http://localhost:8000/login', { username, password });
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
        response = await axios.get('http://localhost:8000/users');
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
    delete axios.defaults.headers.common['Authentication'];
    router.push('/login');
}

async function getAll() {
    const users = await axios.get('http://localhost:8000/users');
    return users.data;
}

/**
 * Save Login token for Later and set all http calls to use it
 * @param token
 */
function setLoginToken(token: string) {
    localStorage.setItem('token', token);
    axios.defaults.headers.common['Authentication'] = token;
}



export const userService = {
    login,
    setLoginToken,
    register,
    logout,
    getAll
};
