<script>
import { RouterLink } from 'vue-router';

export default {
  name: "Login",
  data() {
    return {
      registerActive: false,
      emailLogin: '',
      passwordLogin: '',
      nameReg: '',
      lastnameReg: '',
      emailReg: '',
      passwordReg: '',
      confirmReg: '',
      roleReg : '',
      tipoReg: '',
      emptyFields: false,
    };
  },
  created() {
    // Para testeo
    this.emailReg = "adrian.sandoval@utec.edu.pe"
    this.nameReg = "Adrian Sandoval Huamaní"
    this.roleReg = "Administrador"
  },

  methods: {
    doLogin() {
      if (this.emailLogin === '' || this.passwordLogin === '') {
        this.emptyFields = true;
      } else {
        // Autenticación exitosa, guarda el correo en Local Storage
        // localStorage.setItem('email', this.emailLogin);
        // alert('You are now logged in');
        this.$router.push('/dashboard');
      }
    },
    // doRegister() {
    //   if (
    //     this.emailReg === '' ||
    //     this.nameReg === '' ||
    //     this.lastnameReg === '' ||
    //     this.passwordReg === '' ||
    //     this.confirmReg === '' ||
    //     this.tipoReg === ''
    //   ) {
    //     this.emptyFields = true;
    //   } else {
    //   // Registro exitoso, guarda el correo en Local Storage
    //   localStorage.setItem('email', this.emailReg);
    //   alert('You are now registered');
    //   this.$router.push('/dashboard');
    // }
    // },
    // toggleRegister() {
    //   this.registerActive = !this.registerActive;
    //   this.emptyFields = false;
    // },
  },
}
</script>


<template>

<div class="login-page">
    <div class="custom-container">
      <div v-if="!registerActive" class="card login" :class="{ 'error': emptyFields }">
        <img src="../svg/feelscan.svg" alt="VitalCheck logo" width="200" height="70" />
        <h1>Iniciar sesión</h1>
        <div class="form-group">
          <label class="error-message" v-if="emptyFields && emailLogin === ''">Por favor ingresa tu correo</label>
          <input v-model="emailLogin" type="text" class="form-control" placeholder="Correo" required />
          <label class="error-message" v-if="emptyFields && passwordLogin === ''">Por favor ingresa tu contraseña</label>
          <input v-model="passwordLogin" type="password" class="form-control" placeholder="Contraseña" required />

          <!-- <button type="submit" class="button-68" @click="doLogin">Entrar</button> -->
          <button type="submit" class="button-68" >
          <!-- @click="doLogin"> -->
          
          <!-- <router-link to="/dashboard">Entrar</router-link></button> -->
          <router-link :to="`/dashboard/${nameReg}/${emailReg}/${roleReg}`">
            Entrar
          </router-link>
          </button>

          <!-- <p>¿No tienes una cuenta? <a href="javascript:void(0)" @click="toggleRegister">Crear cuenta</a></p> -->
          <!-- <p><a href="javascript:void(0)">¿Olvidaste tu contraseña?</a></p> -->
        </div>
      </div>

      <!-- <div v-if="registerActive" class="card register" :class="{ 'error': emptyFields }">
        <img src="../svg/feelscan.svg" alt="VitalCheck logo" width="200" height="70" />
        <h1>Registrarse</h1>
        <div class="form-group">
          <label class="error-message" v-if="emptyFields && nameReg === ''">Por favor ingresa tu nombre</label>
          <input v-model="nameReg" type="text" class="form-control" placeholder="Nombre" required />
          <label class="error-message" v-if="emptyFields && lastnameReg === ''">Por favor ingresa tu apellido</label>
          <input v-model="lastnameReg" type="text" class="form-control" placeholder="Apellido" required />
          <label class="error-message" v-if="emptyFields && emailReg === ''">Por favor ingresa tu correo</label>
          <input v-model="emailReg" type="email" class="form-control" placeholder="Correo" required />
          <label class="error-message" v-if="emptyFields && passwordReg === ''">Por favor ingresa tu contraseña</label>
          <input v-model="passwordReg" type="password" class="form-control" placeholder="Contraseña" required />
          <label class="error-message" v-if="emptyFields && confirmReg === ''">Por favor confirma tu contraseña</label>
          <input v-model="confirmReg" type="password" class="form-control" placeholder="Confirmar Contraseña" required />
          <br /> -->
          <!-- <button type="submit" class="button-68" @click="doRegister">Registrar</button>
          <button type="submit" class="button-68"> <RouterLink to="/dashboard"> Registrar </RouterLink></button>
          <p>¿Ya tienes una cuenta? <a href="javascript:void(0)" @click="toggleRegister">Iniciar sesión</a></p>
        </div> -->
      <!-- </div> -->
    </div>
  </div>

</template>


<style scoped>
p {
  line-height: 1rem;
}

img {
  margin-left: 180px;
}

a, h1 {
  color: white;
}

.card {
  padding: 20px;
}

.form-group input {
  margin-bottom: 20px;
}

.error {
  animation-name: errorShake;
  animation-duration: 0.3s;
}

@keyframes errorShake {
  0% {
    transform: translateX(-25px);
  }
  25% {
    transform: translateX(25px);
  }
  50% {
    transform: translateX(-25px);
  }
  75% {
    transform: translateX(25px);
  }
  100% {
    transform: translateX(0);
  }
}

.error-message {
  color: #f4fab2;
  font-size: 22px;
}

/* Media query para dispositivos más pequeños como tabletas */
@media (max-width: 768px) {
  .custom-container {
    width: 90%;
    padding: 20px;
  }
}

/* Media query para dispositivos móviles */
@media (max-width: 480px) {
  .custom-container {
    padding: 10px;
  }

  .form-control {
    max-width: 80%;
    width: 80%;
  }

  .input-control {
    width: 80%;
    margin-left: 0;
    margin-top: 10px;
  }

  img {
    margin-left: 0;
  }
}
</style>