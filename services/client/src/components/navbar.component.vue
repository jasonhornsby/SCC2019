<template>
    <nav>
        <router-link to="/" class="brand">SCC</router-link>

        <div class="title">
            {{ title }}
        </div>

        <div class="login">
            <router-link to="/login" class="btn">Login</router-link>
            <router-link to="/register" class="btn">Register</router-link>
        </div>
    </nav>
</template>
<script lang="ts">
    import Component from 'vue-class-component';
    import Vue from 'vue';

    @Component({
        name: 'navbar'
    })
    export default class NavbarComponent extends Vue {
        get title() {
            return this.$store.getters.getTitle;
        }
    }
</script>
<style lang="scss">
    nav {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        margin-bottom: 20px;
        align-items: center;

        .brand {
            font-size: 1.3rem;
            text-decoration: none;
            color: inherit;
            font-weight: 600;
            flex: 1;
        }

        .login {
            flex: 1;
            display: flex;
            flex-direction: row-reverse;
            &>* {
                margin-left: 10px;
            }
        }
    }
</style>
