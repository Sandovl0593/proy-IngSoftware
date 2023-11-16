<script>
import { RouterView } from 'vue-router';
import Sidebar from './Sidebar.vue';
import Dashboard from './Dashboard.vue';
import SideUser from './SideUser.vue';

export default {
    name: "ViewLogged",
    data() {
        return {
          emailReg: "",
          role: "",
          nameReg: ""
        }
    },
    async created() {
        const params = this.$route.params
        this.nameReg = params.name
        this.emailReg = params.email
        this.role = params.role
        this.tenant_id = params.tid
        
    },

    computed: {
        notWelcome() { return this.$route.path !== "/welcome" },
        in_dashboard() { return this.$route.path.includes("/dashboard") }
    },
    components: { Sidebar, Dashboard, RouterView, SideUser }
    
}
</script>


<template>

    <Sidebar v-if="notWelcome" :nameReg="nameReg" :emailReg="emailReg"/>

    <Dashboard v-if="in_dashboard" :username="nameReg" :email="emailReg" :tid="tenant_id"/>
    <router-view v-if="!in_dashboard"/>

    <SideUser v-if="notWelcome" :nameReg="nameReg" 
                               :emailReg="emailReg" :role="role"/>


</template>
