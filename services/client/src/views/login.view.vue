<template>
    <div class="auth-wrapper">
        <form @submit="checkForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" v-model="username" class="form-control"/>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" class="form-control"/>
            </div>

            <button class="btn btn-block btn-dark" type="submit"> Login </button>
        </form>
    </div>
</template>
<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';
    import { userService } from '@/services/user.service';

    @Component({
        name: 'LoginVue'
    })
    export default class LoginVue extends Vue {

        public errors: any = {};
        public username: string = "";
        public password: string = "";

        mounted() {
            this.$store.commit('changeTitle', 'Login');
        }

        public checkForm($event: any) {
            // Reset errors
            this.errors = [];

            if (this.password && this.password) {
                this.$store.dispatch('login', { username: this.username, password: this.password })
            }

            if (!this.username) {
                this.errors.username = 'Please enter a username';
            }

            if (!this.password) {
                this.errors.password = 'Please enter your password';
            }

            $event.preventDefault();
        }
    }
</script>
<style lang="scss">

</style>
