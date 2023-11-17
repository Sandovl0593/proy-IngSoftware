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
        <router-link class="sidenav-nav-link" :to="`/dashboard/${$props.tenant_id}/${$props.code}/${$props.role}`" exact>
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

      <li @click="showNotifications = true" class="sidenav-nav-item">
        <div class="sidenav-nav-link">
          <img src="../svg/notification.svg" type="image/svg+xml" loading="lazy" class="sidenav-link-icon" />
          <span class="sidenav-link-text" v-if="collapsed">Notification</span>
        </div>
      </li>
    </ul>
  </div>

  <!-- Teleport is Vue3 component for modals -->
  <Teleport to="body">
    <div v-if="showNotifications" class="modal window-not">
      <div class="window-content">
        <button @click="showNotifications = false" class="close" id="closewindow">&times;</button>
        <h2>Miembros no atendidos</h2>
        <ul id="miembrosNoAtendidos">
          <li v-for="(miembro, index) in miembrosNoAtendidos" :key="index">
            {{ miembro }}
          </li>
        </ul>
      </div>
    </div>
  </Teleport>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: "Sidebar",
  props: {
    tenant_id: String,
    code: String,
    role: String
  },
  setup(props) {
    const miembrosNoAtendidos = ref([]);

    const obtenerMiembrosNoAtendidos = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/obtener_miembros_no_atendidos/${props.tenant_id}`);
        const data = await response.json();

        miembrosNoAtendidos.value = data.content;
      } catch (error) {
        console.error('Error al obtener miembros no atendidos:', error);
      }
    };

    onMounted(() => {
      obtenerMiembrosNoAtendidos();
    });

    const collapsed = ref(false);
    const showNotifications = ref(false);
    const screenWidth = ref(window.innerWidth);

    const toggleCollapse = () => {
      collapsed.value = !collapsed.value;
    };

    const closeSidenav = () => {
      collapsed.value = false;
    };

    const onResize = () => {
      screenWidth.value = window.innerWidth;
      if (screenWidth.value > 768) {
        collapsed.value = false;
      }
    };

    window.addEventListener("resize", onResize);

    return {
      miembrosNoAtendidos,
      toggleCollapse,
      closeSidenav,
      onResize,
      collapsed,
      showNotifications,
      screenWidth
    };
  }
};
</script>

<style scoped>
/* Tu estilo existente aquí... */
</style>
