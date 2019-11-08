import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import Vue from 'vue';
import router from '@/router';

@Module
export default class Auth extends VuexModule {

    username: string;
    token: string;
    id: number;

    /**
     * Return boolean based on login state
     */
    get isLoggedIn() {
        return !!this.token;
    }

    /**
     * Fetches the user to be displayed on the site
     */
    get user() {
        return {
            username: this.username,
            id: this.id
        }
    }

    // TODO: Add Response Types
    @Mutation
    login(res: any) {
        const { token, username, id } = res;
        this.username = username;
        this.token = token;
        this.id = id;
        return;
    }


    @Mutation
    logout() {
        this.username = '';
        this.token = '';
        delete this.id;
    }

    @Action({ commit: 'logout' })
    doLogout() {
        delete Vue.axios.defaults.headers.common['Authorization'];
        localStorage.removeItem('token');
        router.push('/login');
        return;
    }

    /**
     * Adds authorization header to axios
     * Sets localstorage token
     * Changes route to homepage
     * @param res
     */
    @Action({ commit: 'login' })
    doLogin(res: any) {
        Vue.axios.defaults.headers.common['Authorization'] = res.token;
        localStorage.setItem('token', res.token);
        return res;
    }

}
