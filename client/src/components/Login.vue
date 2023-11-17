<script>
import axios from 'axios';

export default {
  name: "Login",
  data() {
    return {
      // registerActive: false,
      code: '',
      passwordLogin: '',
      
      // nameReg: '',
      // emailReg: '',
      roleReg : '',
      tenant_id: '',
      
      emptyFields: false,
      messageError: ""
    };
  },
  created() {
  },

  methods: {
    async doLogin() {
      if (this.code === '' || this.passwordLogin === '') {
        this.emptyFields = true;
      } else {
        
        //// peticion post para info de los datos
        //// del correo retorna la id, tenant_id, nombre y rol
        //// y verificando el password

        
        await axios.get(
          `http://127.0.0.1:8000/user/${this.code}/${this.passwordLogin}`, 
          ).then(res => {
            
            this.tenant_id = res.data.tenant_id
            this.roleReg = res.data.rol
            this.$router.push(`/dashboard/${this.tenant_id}/${this.code}/${this.roleReg}`);
            
          }).catch(err => {
            this.messageError = err.response.data.error
          })

        }
    }
  }
}
</script>


<template>

<div class="login-page">
    <div class="custom-container">
      <div v-if="!registerActive" class="card login" :class="{ 'error': emptyFields }">
        <img src="../svg/feelscan.svg" alt="VitalCheck logo" width="200" height="70" />
        <h1>Iniciar sesión</h1>

        <form class="form-group" @submit.prevent="doLogin()">
          <label class="error-message" v-if="emptyFields && code === ''">Por favor ingresa tu código</label>
          <input v-model="code" type="text" class="form-control" placeholder="Código" required />

          <label class="error-message" v-if="emptyFields && passwordLogin === ''">Por favor ingresa tu contraseña</label>
          <input v-model="passwordLogin" type="password" class="form-control" placeholder="Contraseña" required />

          <label class="error-message" v-if="messageError"> {{ messageError }}</label>
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