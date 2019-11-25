<template>
    <div class="notification-wrapper">
        <div
                class="alert"
                role="alert"
                v-for="notification of notifications"
                v-bind:key="notification.id"
                v-bind:class="{ 'alert-danger': notification.type === 'error', 'alert-primary': notification.type === 'alert'  }"
        >
            {{ notification.name }}
        </div>
    </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import Component from 'vue-class-component';

    @Component({
        name: 'Notification'
    })
    export default class NotificationComponent extends Vue {

        get notifications() {
            return this.$store.getters.notifications;
        }

    }

</script>

<style lang="scss">
.notification-wrapper {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 5px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
