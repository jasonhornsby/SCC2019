import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { userService } from '@/services/user.service';

@Module
export default class UserStore extends VuexModule {

    loading: boolean = false;
    error: string;
    all: any;

    @Action
    async loadUsers() {
        let users;
        try {
            users = await userService.getAll();
        } catch (e) {
            this.context.commit('getAllFailure', e);
            return
        }
        this.context.commit('getAllSuccess', users);
    }

    @Mutation
    getAllRequest() {
        this.loading = true;
    }

    @Mutation
    getAllSuccess(users: any) {
        this.all = users;
    }

    @Mutation
    getAllFailure(error: any) {
        this.error = error;
    }

}
