<script>
import ViewLogged from './components/ViewLogged.vue';
import Login from './components/Login.vue';

export default {  
  name: "App",
  computed: {
    in_login() {
      return this.$route.path === '/login' || this.$route.path === '/';
    }
  },
  components: { ViewLogged, Login }
}

</script>

<template>
 
  <Login v-if="in_login"/>

  <ViewLogged v-if="!in_login"/>

</template>
