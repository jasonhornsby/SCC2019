<template>
    <div class="auth-wrapper">
        <form @submit="checkForm">
            <div class="form-element">
                <div class="label">
                    <label for="username">Username</label>
                </div>
                <div class="input">
                    <input type="text" id="username" v-model="username"/>
                    <span v-if="errors.username">{{ errors.username }}</span>
                </div>
            </div>
            <div class="form-element">
                <div class="label">
                    <label for="password">Password</label>
                    <span v-if="errors.password">{{ errors.password }}</span>
                </div>
                <div class="input">
                    <input type="password" id="password" v-model="password"/>
                </div>
            </div>
            <div class="form-element">
                <div class="label"></div>
                <span v-if="errors.server">{{ errors.server }}</span>
                <button type="submit" class="btn input">Register</button>
            </div>
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

        public errors: any = {};
        public username: string = "";
        public password: string = "";

        mounted() {
            this.$store.commit('changeTitle', 'Register');
        }


        public checkForm($event: any) {
            // Reset errors
            this.errors = {
                'username': null,
                'password': null,
                'server': null
            };

            if (this.password && this.password) {
                this.axios.post('http://localhost:8000/register', {
                    username: this.username,
                    password: this.password
                }).then(res => {
                    this.$store.dispatch('doLogin', res.data);
                    return;
                }).catch((error) => {
                    console.log(error.response.status);
                    if (error.response.status === 401 || error.response.status === 409) {
                        this.errors.server = error.response.data.message;
                    }
                    return;
                })
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

