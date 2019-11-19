import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { userService } from '@/services/user.service';
import router from '@/router';

const user = JSON.parse(localStorage.getItem('user') as string) || null;

@Module
export default class Auth extends VuexModule {

    public user = user;
    public error: any = null;
    public loading: boolean = false;

    get isLoggedIn() {
        return !!this.user;
    }

    @Action({ rawError: true })
    async login(payload: { username: any, password: any}) {
        let user;
        try {
            user = await userService.login(payload.username, payload.password);
        } catch (e) {
            this.context.commit('loginFailure', e);
            this.context.commit('newNotification', { name: e.message, type: 'error'});
            return;
        }
        this.context.commit('loginSuccess', user);
        this.context.commit('newNotification', { name: 'Successfully logged in', type: 'alert'});
        return user;
    }

    @Action({ rawError: true })
    async register(payload: { username: string, password: string }) {
        let user;
        try {
            user = await userService.register(payload.username, payload.password);
        } catch (e) {
            this.context.commit('loginFailure', e);
            this.context.commit('newNotification', { name: e.message, type: 'error'});
            return;
        }
        this.context.commit('loginSuccess', user);
        this.context.commit('newNotification', { name: 'Successfully logged in', type: 'alert'});
        return user;
    }

    @Action
    doLogout() {
        userService.logout();
        this.context.commit('logout');
    }

    @Mutation
    loginRequest(user: any) {
        this.loading = true;
    }

    @Mutation
    loginSuccess(user: any) {
        this.loading = false;
        this.user = {
            id: user.id,
            username: user.username,
        };

        localStorage.setItem('user', JSON.stringify(this.user));
        userService.setLoginToken(user.token);
        router.push('/');
    }

    @Mutation
    loginFailure(error: Error) {
        this.loading = false;
        this.error = error.message;
    }

    @Mutation
    logout() {
        this.loading = false;
        this.user = false;
        this.error = false;
    }

}
