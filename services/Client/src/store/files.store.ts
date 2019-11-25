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

    get getFile(): any {
        return (id: number) => {
            return this.files.find(file => file.id === id) || null;
        }
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
    async fetchFile(id: number) {
        this.context.commit('startLoading');
        let file = await fileService.getFile(id);
        this.context.commit('addFile', file);
    }

    @Action({ rawError: true })
    async fetchFiles() {
        this.context.commit('startLoading');
        let files = await fileService.getFiles();
        this.context.commit('setFiles', files);
    }

    @Mutation
    addFile(file: IFile) {
        this.files.push(file);
    }
}
