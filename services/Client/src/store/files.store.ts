import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';
import { fileService } from '@/services/file.service';
import { IFile } from '@/models/file.model';

@Module
export default class FilesStore extends VuexModule {

    public loading: boolean = false;
    public files: IFile[] = [];

    get getFiles() {
        return this.files;
    }

    @Mutation
    startLoading() {
        this.loading = true;
    }

    @Mutation
    setFiles(files: any[]) {
        this.files = files;
        this.loading = false;
    }

    @Action({ rawError: true })
    async fetchFiles() {
        this.context.commit('startLoading');
        let files = await fileService.getFiles();
        this.context.commit('setFiles', files);
    }
}
