<script>
import axios from 'axios';

export default {
  name: "Login",
  data() {
    return {
      // registerActive: false,
      emailLogin: '',
      passwordLogin: '',
      
      nameReg: '',
      emailReg: '',
      roleReg : '',
      tenant_id: '',
      
      emptyFields: false,
    };
  },
  created() {
  },

  methods: {
    async doLogin() {
      if (this.emailLogin === '' || this.passwordLogin === '') {
        this.emptyFields = true;
      } else {
        
        //// peticion post para info de los datos
        //// del correo retorna la id, tenant_id, nombre y rol
        //// y verificando el password

        /*
        await axios.post(
          "http://127.0.0.1:8000/Nmembers/", 
          { email: this.emailLogin, password: this.passwordLogin },
          { 'Content-Type': 'application/json' }
          ).then(res => {
          this.nameReg  = res.data.name;
          this.emailLogin = res.data.email
          this.roleReg = res.data.rol,
          
        }).catch(err => {
          // Para testeo
          */
         // this.passwordLogin = 'aaa'
         
         this.nameReg = "Adrian Sandoval Huamaní"
         this.roleReg = "Psicologo"
         this.tenant_id = "UTEC"
        // })
        
        this.$router.push(`/dashboard/${this.tenant_id}/${this.nameReg}/${this.emailLogin}/${this.roleReg}`);
      }
    },
  },
}
</script>


<template>

<div class="login-page">
    <div class="custom-container">
      <div v-if="!registerActive" class="card login" :class="{ 'error': emptyFields }">
        <img src="../svg/feelscan.svg" alt="VitalCheck logo" width="200" height="70" />
        <h1>Iniciar sesión</h1>

        <form class="form-group" @submit.prevent="doLogin()">
          <label class="error-message" v-if="emptyFields && emailLogin === ''">Por favor ingresa tu correo</label>
          <input v-model="emailLogin" type="text" class="form-control" placeholder="Correo" required />

          <label class="error-message" v-if="emptyFields && passwordLogin === ''">Por favor ingresa tu contraseña</label>
          <input v-model="passwordLogin" type="password" class="form-control" placeholder="Contraseña" required />

          <button type="submit" class="button-68" >
            Entrar
          </button>

          <!-- <p>¿No tienes una cuenta? <a href="javascript:void(0)" @click="toggleRegister">Crear cuenta</a></p> -->
          <!-- <p><a href="javascript:void(0)">¿Olvidaste tu contraseña?</a></p> -->
        </form>
      </div>
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