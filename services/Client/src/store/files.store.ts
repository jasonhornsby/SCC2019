import { Action, Module, Mutation, VuexModule } from 'vuex-module-decorators';
import { fileService } from '@/services/file.service';
import { IFile } from '@/models/file.model';

export interface IFilesStore {
    own_files: IFile[],
    shared_files: IFile[]
}

@Module
export default class FilesStore extends VuexModule {

    public loading: boolean = false;
    public files: IFilesStore = { shared_files: [], own_files: [] };

    get getFiles() {
        return this.files;
    }

    get getFile(): any {
        return (id: number) => {
            const ownFile = this.files.own_files.find(file => file.id === id);
            const sharedFile = this.files.shared_files.find(file => file.id === id);
            return ownFile || sharedFile || null;
        }
    }

    @Mutation
    startLoading() {
        this.loading = true;
    }

    @Mutation
    stopLoading() {
        this.loading = false;
    }

    @Mutation
    setFiles(files: IFilesStore) {
        this.files = files;
        this.loading = false;
    }

    @Action({ rawError: true })
    async fetchFile(id: number) {
        this.context.commit('startLoading');
        let file = await fileService.getFile(id);
        this.context.commit('addFile', file);
        this.context.commit('stopLoading');
    }

    @Action({ rawError: true })
    async fetchFiles() {
        this.context.commit('startLoading');
        let files = await fileService.getFiles();
        if (!files.own_files) {
            files.own_files = [];
        }
        if(!files.shared_files) {
            files.shared_files = [];
        }
        this.context.commit('setFiles', files);
    }

    @Mutation
    addFile(file: IFile) {
        const ownFile = this.files.own_files.find(file => file.id === file.id);
        const sharedFile = this.files.shared_files.find(file => file.id === file.id);
        if (!ownFile || !sharedFile) {
            if (file._shared_with == "") {
                this.files.own_files.push(file);
            } else {
                this.files.shared_files.push(file);
            }
        }
    }

    @Action
    deleteFile(file: IFile) {

    }

}
