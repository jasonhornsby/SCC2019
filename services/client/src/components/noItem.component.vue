<template>
    <div class="alert alert-primary text-center">{{ message }}</div>
</template>
<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';
    import { Prop } from 'vue-property-decorator';

    @Component
    export default class NoItem extends Vue {
        @Prop()
        public message;
    }
</script>
