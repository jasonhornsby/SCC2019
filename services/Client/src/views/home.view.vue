<template>
    <div class="files-wrapper row" ref="body">
        <aside class="file-upload col-12 col-md-3 pb-1 pb-md-0">
            <button class="btn btn-dark" @click="triggerUpload()">Upload new File</button>
            <input type="file" ref="upload" class="invisible" v-on:change="handleSubmitFile()"/>
        </aside>

        <main class="files-list col-12 col-md-9">

            <div class="progress mb-2" v-if="uploading">
                <div class="progress-bar" role="progressbar" v-bind:style="{ width: uploadedPercent + '%' }" aria-valuemin="0" aria-valuemax="100" ref="progress">{{ uploadedPercent }}%</div>
            </div>

            <no-item v-if="files.length === 0" message="No files uploaded"></no-item>

            <ul class="list-group">
                <li class="list-group-item"
                    v-for="file in files"
                    v-bind:key="file.id"
                    @click="goToFile(file.id)"
                >
                    {{ file.name }}
                    <span class="badge badge-primary badge-pill float-right">{{ humanFileSize(file.size) }}</span>
                </li>
            </ul>
        </main>
    </div>
</template>

<script lang="ts">
    import Vue from "vue";
    import Component from "vue-class-component";
    import axios from "axios";
    import NoItem from "@/components/noItem.component.vue";
    import { fileServiceURL } from "@/services/file.service";

    @Component({
        name: 'HomeView',
        components: { NoItem }
    })
    export default class HomeView extends Vue {

        uploading: boolean = false;
        uploadedPercent: number = 0;

        $refs: any;

        get files() {
            return this.$store.getters.getFiles;
        }

        mounted() {
            this.$store.commit('changeTitle', 'My files');
            this.$store.dispatch('fetchFiles');
        }

        goToFile(id: number) {
            this.$router.push(`/file/${ id }`);
        }
        humanFileSize(size: number) {
            if (size < 1024) return size + ' B';
            let i = Math.floor(Math.log(size) / Math.log(1024));
            let num: any = (size / Math.pow(1024, i));
            let round = Math.round(num);
            num = round < 10 ? num.toFixed(2) : round < 100 ? num.toFixed(1) : round;
            return `${num} ${'KMGTPEZY'[i-1]}B`
        }


        triggerUpload() {
            this.$refs.upload.click();
        }

        handleSubmitFile() {
            // Get the uploaded file
            let file: File = this.$refs.upload.files[0];

            // Create Upload form data
            let formData = new FormData();
            formData.append('file_content', file);

            // Reset upload UI
            this.uploading = true;
            this.uploadedPercent = 0;

            // Send the request
            axios.post(
                fileServiceURL,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    onUploadProgress: this.handleUploadProgress,
                }
            )
                .then(val => {
                    this.uploading = false;
                    this.$store.commit('newNotification', {
                        name: `File successfully uploaded`,
                        type: 'alert'
                    });
                    this.$store.commit('addFile', val.data);
                })
                .catch(err => {
                    this.uploading = false;
                    this.$store.commit('newNotification', {
                        name: `File "${ file.name }" failed to upload. Please try again.`,
                        type: 'error'
                    })
                });
        }

        /**
         * Handle Upload Progress and update state
         * @param progress
         */
        handleUploadProgress(progress: ProgressEvent) {
            if (!progress.lengthComputable) {
                return;
            }
            this.uploadedPercent = Math.round(progress.loaded / progress.total * 100);
        }
    }
</script>

<style lang="scss">

    .file-upload {
        button {
            width: 100%;
        }
    }

    .list-group-item {
        cursor: pointer;
        &:hover {
            background-color: rgba(0,0,0,0.03);
        }
    }
</style>
