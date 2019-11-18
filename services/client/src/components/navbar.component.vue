<template>
    <nav class="navbar navbar-light mb-3">
        <router-link to="/" class="navbar-brand">SCC</router-link>

        <div class="title">
            {{ title }}
        </div>

        <div class="login">
            <button class="btn btn-dark" @click="logout()" v-if="isLoggedIn">Logout</button>
            <router-link to="/login" class="btn btn-dark" v-if="!isLoggedIn">Login</router-link>
            <router-link to="/register" class="btn btn-outline-dark" v-if="!isLoggedIn">Register</router-link>
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

        get isLoggedIn() {
            return this.$store.getters.isLoggedIn;
        }

        logout() {
            this.$store.dispatch('doLogout');
        }
    }
</script>
<style lang="scss">
    .navbar-brand {
        font-weight: bolder;
    }
    .login {
        .btn {
            margin-left: 10px;
        }
    }
</style>
