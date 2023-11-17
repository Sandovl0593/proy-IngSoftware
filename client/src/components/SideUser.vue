<script>

export default {
    name: "SideUser",
    props: {
     // state log up user
      code: String,
      nameReg: String,
      role: String,
      emailReg: String
    },
    
    data() {
      return {

        screenWidth: window.innerWidth,
        collapsed_user: false,

      };
    },
    methods: {
        toggleCollapseUser() {
            this.collapsed_user = !this.collapsed_user;
        },
        closeSidenavUser() {
            this.collapsed_user = false;
        },

        
    },
}
</script>


<template>
  
  <div id="box-left-sidenav"  style="direction: rtl;">
    <div :class="['sidenav-left', collapsed_user ? 'sidenav-collapsed-left' : '']">
      <div style="display: flex;">
        <button class="logo-user" @click="toggleCollapseUser()">
          <img src="../svg/user.svg" width="50" type="image/svg+xml" loading="lazy" class="sidenav-link-icon" />
        </button>

        <div id="box-user-info" v-if="collapsed_user">
          <div>{{ $props.code }}</div>
          <div>{{ $props.nameReg }}</div>
          <div>{{ $props.emailReg }}</div>
          <div>{{ $props.role }}</div>
        </div>

        <button class="btn-close" v-if="collapsed_user && screenWidth <= 768" @click="closeSidenavUser()">
          <i class="fal fa-times close-icon"></i>
        </button>
      </div>
    </div>
  </div>
</template>
