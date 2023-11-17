<script>
import { RouterView } from 'vue-router';
import Sidebar from './Sidebar.vue';
import Dashboard from './Dashboard.vue';
import SideUser from './SideUser.vue';

export default {
    name: "ViewLogged",
    data() {
        return {
          code: "",  
          emailReg: "",
          role: "",
          nameReg: "",
          tenant_id: "",
        }
    },
    async created() {
        const params = this.$route.params

        this.code = params.code
        this.role = params.role
        this.tenant_id = params.tid

        // aqui se obtiene el nombre y correo de usuario

        // test
        this.nameReg = "Verónica Lunga"
        this.emailReg = "verónica.lunga@utec.edu.pe"
        
    },

    computed: {
        notWelcome() { return this.$route.path !== "/welcome" },
        in_dashboard() { return this.$route.path.includes("/dashboard") }
    },
    components: { Sidebar, Dashboard, RouterView, SideUser }
    
}
</script>


<template>

    <Sidebar v-if="notWelcome" :code="code" :role="role" :tid="tenant_id"/>

    <Dashboard v-if="in_dashboard" :username="nameReg" :email="emailReg" :tid="tenant_id" :role="role"/>
    <router-view v-if="!in_dashboard"/>

    <SideUser v-if="notWelcome" :nameReg="nameReg" 
                               :code="code" :role="role" :email="emailReg"/>


</template>
