import { Module, Mutation, VuexModule } from 'vuex-module-decorators';

export interface INotification {
    name: string;
    id: number;
    type: 'alert' | 'error';
}

@Module
export default class NotificationStore extends VuexModule {

    all: INotification[] = [];

    get notifications() {
        return this.all;
    }

    @Mutation
    newNotification(payload: { name: string, type: 'alert' | 'error' }) {
        const id = Math.random();
        this.all.push({
            name: payload.name,
            type: payload.type,
            id: id
        });

        // Close timeout after specific time
        setTimeout(() => {
            const index = this.all.findIndex(notification => notification.id === id);
            this.all.splice(index, 1);
        }, 1000)
    }

    @Mutation
    closeMutation(payload: number) {
        const index = this.all.findIndex(notification => notification.id === payload);
        this.all.splice(index, 1);
    }

}
