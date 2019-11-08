<template>
    <div class="register">
        <h1>Register a new account</h1>
        <span v-for="(error, index) in errors" v-bind:key="index">{{ error }}</span>
        <form
                @submit="checkForm"
        >
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username"/>

            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password"/>

            <button type="submit">Register</button>
        </form>
    </div>
</template>
<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';

    @Component({
        name: 'RegisterView'
    })
    export default class RegisterView extends Vue {

        public errors: string[] = [];
        public username: string = "";
        public password: string = "";

        public checkForm($event: any) {
            // Reset errors
            this.errors = [];

            if (this.password && this.password) {
                this.axios.post('http://localhost:8000/register', {
                    username: this.username,
                    password: this.password
                }).then(res => {
                    this.$store.dispatch('doLogin', res.data);
                    return;
                }).catch((error) => {
                    if (error.response.status === 401) {
                        this.errors.push(error.response.data.message);
                    }
                    return;
                })
            }

            if (!this.username) {
                this.errors.push('Please enter a username');
            }

            if (!this.password) {
                this.errors.push('Please enter your password');
            }

            $event.preventDefault();
        }
    }
</script>

