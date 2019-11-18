<template>
    <div class="files-wrapper">
        <aside class="file-upload">
            <button class="btn btn-dark">Upload new File</button>
        </aside>

        <main class="files-list">
            <ul class="list-group">
                <li class="list-group-item"
                    v-for="file in files"
                    v-bind:key="file.id"
                    @click="selectFile(file.id)"
                    :class="{'active' : selectedFile && selectedFile.id === file.id}"
                >
                    {{ file.name }}
                    <span class="badge badge-primary badge-pill">{{ file.size }}</span>
                </li>
            </ul>
        </main>

        <aside class="files-description" v-if="selectedFile">
            <h1>{{ selectedFile.name }}</h1>
        </aside>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';

    @Component({
        name: 'HomeView'
    })
    export default class HomeView extends Vue {

        files = [
            {
                id: 1,
                name: 'My first file',
                uploaded: '22.03.2019',
                size: '3mb'
            },
            {
                id: 2,
                name: 'My second file',
                uploaded: '22.03.2019',
                size: '3mb'
            },
            {
                id: 3,
                name: 'My third file',
                uploaded: '22.03.2019',
                size: '3mb'
            }
        ];

        selectedFile: any = null;

        mounted() {
            this.$store.commit('changeTitle', 'My files');
        }

        selectFile(id: number) {
            let newSelection = this.files.find(file => file.id === id);
            if (newSelection === this.selectedFile) {
                this.selectedFile = null;
            } else {
                this.selectedFile = newSelection;
            }
        }
    }
</script>



<style lang="scss">
    .files-wrapper {
        display: flex;
        flex-direction: row;
        &>* {
            padding: 0px 5px;
            &:first-child {
                padding-left: 0;
            }
            &:last-child {
                padding-right: 0;
            }
        }
        .files-list {
            flex: 1;

            .file {
                display: flex;
                background-color: white;
                padding: 10px 10px;
                align-items: center;
                margin-bottom: 5px;
                cursor: pointer;
                box-shadow: 0 6px 8px rgba(102,119,136,.03), 0 1px 2px rgba(102,119,136,.3);

                &.selected {
                    background: linear-gradient(15deg,#678,#6f8793);
                    color: white;
                }

                .name {
                    flex: 1;
                    font-size: 1.1rem;
                }
                .size {
                    flex-basis: 50px;
                    text-align: end;
                }
            }
        }
        .file-upload {
            flex-basis: 200px;
            .btn {
                width: 100%;
            }
        }
        .files-description {
            flex-basis: 200px;
            background-color: white;
            padding: 10px 10px;
            box-shadow: 0 6px 8px rgba(102,119,136,.03), 0 1px 2px rgba(102,119,136,.3);
            h1 {
                margin: 0;
            }
        }
    }
</style>
