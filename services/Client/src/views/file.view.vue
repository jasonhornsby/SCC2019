<template>
    <div class="row">

        <div class="loading-spinner col-12 d-flex justify-content-center" v-if="!file">
            <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>

        <aside class="file-upload col-12 col-md-3 pb-1 pb-md-0" v-if="file">
            <button class="btn btn-primary" @click="downloadFile()" v-bind:disabled="downloading">
                Download File
                <span class="spinner-border spinner-border-sm ml-2" role="status" v-if="downloading">
                    <span class="sr-only">Loading...</span>
                </span>
            </button>


            <button class="btn btn-dark mt-2" @click="deleteFile()">Delete File</button>


        </aside>

        <div class="col-12 col-md-9 col-lg-9" v-if="file">
            <div class="card">
                <div class="card-header">
                    {{ file.name }}
                </div>
                <div class="card-body">
                    Size: {{ humanFileSize(file.size) }}
                </div>
                <div class="progress mb-2" v-if="downloading">
                    <div class="progress-bar" role="progressbar" v-bind:style="{ width: downloadPercent + '%' }" aria-valuemin="0" aria-valuemax="100" ref="progress">{{ downloadPercent }}%</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import { Component } from 'vue-property-decorator';
    import { IFile } from '@/models/file.model';
    import axios from 'axios';
    import { fileServiceURL } from "@/services/file.service";
    import { IFilesStore } from "@/store/files.store";

    @Component({
        name: 'FileView'
    })
    export default class FileView extends Vue {

        downloading = false;
        downloadPercent = 0;

        get file() {
            let files = this.$store.getters.getFiles as IFilesStore;
            const ownFile = files.own_files.find(file => file.id === parseInt(this.$route.params.id));
            const sharedFile = files.shared_files.find(file => file.id === parseInt(this.$route.params.id));
            return ownFile || sharedFile || {} as any;
        }

        mounted() {
            this.$store.dispatch('fetchFile', this.id);
        }

        get id() {
            return parseInt(this.$route.params.id, 10);
        }

        humanFileSize(size: number) {
            if (size < 1024) return size + ' B';
            let i = Math.floor(Math.log(size) / Math.log(1024));
            let num: any = (size / Math.pow(1024, i));
            let round = Math.round(num);
            num = round < 10 ? num.toFixed(2) : round < 100 ? num.toFixed(1) : round;
            return `${num} ${'KMGTPEZY'[i-1]}B`
        }

        downloadFile() {
            this.downloading = true;
            this.downloadPercent = 0;
            axios.get(fileServiceURL + '/' + this.id + '/download' ,
                {
                    responseType: 'blob',
                    onDownloadProgress: this.onDownloadProgress
                })
                .then(({ data }) => {
                    const blob = new Blob([data]);
                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = this.file.name;
                    link.click();
                    this.downloading = false;
                    this.$store.commit('newNotification', {
                        name: 'Files successfully downloaded',
                        type: 'alert'
                    });
                }).catch(e => {
                    this.downloading = false;
                    this.$store.commit('newNotification', {
                        name: 'Failed to download',
                        type: 'error'
                    })
            })
        }
        onDownloadProgress(progress: ProgressEvent) {
            this.downloadPercent = Math.round(progress.loaded / this.file.size * 100);
        }
        deleteFile() {
            axios.delete(fileServiceURL + '/' + this.id).then(res => {
                this.$router.push('/');
                this.$store.commit('newNotification', {
                    name: 'File successfully deleted',
                    type: 'alert'
                });
            });
        }
    }
</script>

<style lang="scss">

</style>
