<script>
import { RouterLink } from 'vue-router';
import { Teleport } from 'vue';

export default {
    name: "Sidebar",
    props: [
      // state log up user
     "nameReg",
      "emailReg",
      "role"
    ],
    data() {
      return {
        // state user

        collapsed: false,
        showNotifications: false,
        screenWidth: window.innerWidth,

        citasPendientes: ["Margiory", "Marcela", "Milloshy", "Fabiola", "Adrian"],
        // citasPendientes: []
      };
    },
    methods: {
        toggleCollapse() {
            this.collapsed = !this.collapsed;
        },
        closeSidenav() {
            this.collapsed = false;
        },
        onResize(event) {
            this.screenWidth = window.innerWidth;
            if (this.screenWidth > 768) {
                this.collapsed = false; // Oculta el sidenav en dispositivos no móviles
            }
        },
        
    },

    mounted() {
        window.addEventListener("resize", this.onResize);
    },
    destroyed() {
        window.removeEventListener("resize", this.onResize);
    },

    components: { Teleport }
}
</script>


<template>
  <div :class="['sidenav', collapsed ? 'sidenav-collapsed' : '']">
    <div class="logo-container">
      <button class="logo" @click="toggleCollapse()"><img src="../svg/feelscan.svg" loading="lazy"></button>
      <div class="logo-text" v-if="collapsed">FeelScan</div>
      <button class="btn-close" v-if="collapsed && screenWidth <= 768" @click="closeSidenav()">
        <i class="fal fa-times close-icon"></i>
      </button>
    </div>

    <ul class="sidenav-nav">
      
      <li class="sidenav-nav-item">
        <router-link class="sidenav-nav-link" :to="`/profile/${$props.nameReg}/${$props.emailReg}/${$props.role}`" exact>
          <img src="../svg/user.svg" type="image/svg+xml" loading="lazy" class="sidenav-link-icon" />
          <span class="sidenav-link-text" v-if="collapsed">Profile</span>
        </router-link>
      </li>

        <li class="sidenav-nav-item">
          <!-- si esta en mismo /dashboard, no hacer nada -->
           <router-link class="sidenav-nav-link" :to="`/dashboard/${$props.nameReg}/${$props.emailReg}/${$props.role}`" exact>
            <img src="../svg/home.svg" type="image/svg+xml" loading="lazy" class="sidenav-link-icon" />
            <span class="sidenav-link-text" v-if="collapsed">Dashboard</span>
          </router-link>
        </li>
  
        <li class="sidenav-nav-item">
          <router-link class="sidenav-nav-link" to="/recommendation" exact>
            <img src="../svg/recommendation.svg" type="image/svg+xml" loading="lazy" class="sidenav-link-icon" />
            <span class="sidenav-link-text" v-if="collapsed">Recommendation</span>
          </router-link>
        </li>

        <li @click="showNotifications = true" class="sidenav-nav-item"><div class="sidenav-nav-link">
            <img src="../svg/notification.svg" type="image/svg+xml" loading="lazy" class="sidenav-link-icon" />
            <span class="sidenav-link-text" v-if="collapsed">Notification</span></div>
        </li>
    </ul>
  </div>

  <!-- Teleport is Vue3 component for modals -->
  <Teleport to="body">   
    <div v-if="showNotifications" class="modal window-not">
      <div class="window-content">
        <button @click="showNotifications = false" class="close" id="closewindow">&times;</button>
        <h2>Tienes citas pendientes!!</h2>
        <ul id="miembrosPendientes">
          <!-- Aquí se agregaría la data a usar sobre las citas de FeelScan? -->
          <li v-for="(integer, index) in citasPendientes" :key="index">
            {{ integer }}
          </li>
        </ul>
      </div>
    </div>
  </Teleport>
</template>
