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

        <aside class="card" v-if="selectedFile">
            <div class="card-header">
                {{ selectedFile.name }}
            </div>
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

        .files-list {
            flex: 1;
            margin-left: 10px;
            margin-right: 10px;
        }
        .file-upload {
            flex-basis: 200px;
            .btn {
                width: 100%;
            }
        }
        aside.card {
            flex-basis: 300px;
            flex-shrink: 0;
        }
    }
</style>
