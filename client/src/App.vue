<script>
import { RouterView } from 'vue-router';
import Sidebar from './components/Sidebar.vue'
// import Notification from './components/Notification  .vue'

export default {  
  name: "App",
  computed: {
    viewNav() {
        return this.$route.path !== '/login' && this.$route.path !== '/welcome';
    },

    in_dashboard() {
      return this.$route.path === '/dashboard' || this.$route.path === '/';
    }
  },
  components: { Sidebar }
}

</script>

<template>
 

  <Sidebar v-if="viewNav"/>

  <router-view />

  <!-- <Notification v-if="in_dashboard" /> -->
  <!--  -->

</template>

<style scoped>

</style>
