<template>
    <div class="auth-wrapper">
        <p v-for="(error, index) in errors" v-bind:key="index" class="text-red-500 text-xs italic">{{ error }}</p>
        <form @submit="checkForm">
            <div class="form-element">
                <div class="label">
                    <label for="username">Username</label>
                </div>
                <div class="input">
                    <input type="text" id="username" v-model="username"/>
                </div>
            </div>

            <div class="form-element">
                <div class="label">
                    <label for="password">Password</label>
                </div>
                <div class="input">
                    <input type="password" id="password" v-model="password"/>
                </div>
            </div>
            <div class="form-element">
                <div class="label"></div>
                <button class="btn input" type="submit"> Login </button>
            </div>
        </form>
    </div>
</template>
<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';

    @Component({
        name: 'LoginVue'
    })
    export default class LoginVue extends Vue {

        public errors: string[] = [];
        public username: string = "";
        public password: string = "";

        mounted() {
            this.$store.commit('changeTitle', 'Login');
        }

        public checkForm($event: any) {
            // Reset errors
            this.errors = [];

            if (this.password && this.password) {
                this.axios.post('http://localhost:8000/login', {
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
<style lang="scss">

</style>
