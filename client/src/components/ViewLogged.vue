<script>
import { RouterView } from 'vue-router';
import Sidebar from './Sidebar.vue';
import Dashboard from './Dashboard.vue';

export default {
    name: "ViewLogged",
    created() {
        const params = this.$route.params
        this.nameReg = params.name
        this.emailReg = params.email
        this.role = params.role
    },
    computed: {
        notWelcome() { return this.$route.path !== "/welcome" },
        in_dashboard() { return this.$route.path.includes("/dashboard") }
    },
    components: { Sidebar, Dashboard }
    
}
</script>


<template>

    <Sidebar v-if="notWelcome" :nameReg="nameReg" 
                               :emailReg="emailReg" :role="role"/>

    <Dashboard v-if="in_dashboard" :username="nameReg" :email="emailReg"/>

    <router-view v-if="!in_dashboard"/>

</template>
