import { Module, VuexModule, Mutation } from 'vuex-module-decorators';

@Module
export default class Title extends VuexModule {

    public title: string = 'SCC';

    get getTitle() {
        return this.title;
    }

    @Mutation
    changeTitle(newTitle: string) {
        this.title = newTitle;
    }

}
