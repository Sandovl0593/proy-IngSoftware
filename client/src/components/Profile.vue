<script>
export default {
  name: "Profile",
  // props: {
  //   username: String,
  //   email: String,
  //   role: String,
  // },

  created() {
    const params = this.$route.params
    this.nameReg = params.name
    this.emailReg = params.email
    this.role = params.role
  }
}
</script>


<template>

<!-- por ahora asumimos que nos logueamos un usuario y este mismo ya autenticado desde Login -->
<section>
    <div class="box-info" id="user-box">
      <div id="img-user">
        <img src="http://" alt="User profile" width="300" />
      </div>
      <div id="section-user">
        <p>Nombre: {{ $route.params.name }}</p>
        <p>Correo: {{ $route.params.email }}  </p>
        <p>Rol: {{ $route.params.role }}</p>
      </div>
    </div>
</section>

</template>


<style scoped>

#user-box {
  display: flex;
  justify-content: space-around;
  height: 50%;
}

#user-box div {
  margin-bottom: 0;
}

</style>