<template>
    <div class="row">
        <div class="col-12 col-md-6 col-lg-4 offset-md-3 offset-lg-4">
            <div class="card">
                <div class="card-header">
                    Name of File, {{ id }}
                </div>
                <div class="card-body">
                    Generall info about the file
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import { Component } from 'vue-property-decorator';

    @Component({
        name: 'FileView'
    })
    export default class FileView extends Vue {
        get id() {
            return this.$route.params.id;
        }
    }
</script>

<style lang="scss">

</style>
