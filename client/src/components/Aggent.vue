<template>

  <div class="container" v-if="showWindow">
    <div id="container-modal">

      <div id="text-aggent">
        <h3>Agende una cita de {{ $props.username }} con nuestros psicólogos</h3>
        <!-- <p>Email: {{ $props.email }}</p> -->
      </div>
      

      <div class="contact-form">
        <form ref="form" @submit.prevent="sendAggent">
          <div class="form-group-table">
            <table>
              <thead>
                <tr>
                  <th>Psicólogo</th>
                  <th>Lunes</th><th>Martes</th>
                  <th>Miercoles</th><th>Jueves</th>
                  <th>Viernes</th>
                </tr>
            </thead>
            <tbody>
              <tr v-for="(horarios, code) in horariosPsico" :key="code">
                <td @click="toCheckPsico(horarios.correo, code)"
                  :style="activeTr(code)" > {{ horarios.nombre }}</td>

                <td > {{ horarios["Lunes"].join("\n")  }}</td>
                <td > {{ horarios["Martes"].join("\n")  }}</td>
                <td > {{ horarios["Miercoles"].join("\n")  }}</td>
                <td > {{ horarios["Jueves"].join("\n")  }}</td>
                <td > {{ horarios["Viernes"].join("\n")  }}</td>
              </tr>
            </tbody>
          </table>
            
          </div> 
          <div class="form-group">
            <input v-model="date" class="form-control" type="date" placeholder="Fecha de visita *" />
          </div>
          <div class="form-group">
            <textarea v-model="message" class="form-control" placeholder="Mensaje *" cols="45" rows="8"></textarea>
          </div>
          <div class="form-group">
            <button class="btn send-button" type="submit" @click="sendEmail()">Enviar</button>
          </div>
          <p v-if="!isFormValid" class="error-message">Por favor, llene todos los campos.</p>
          <div v-if="isEmailSent" class="success-message">
            <p>Correo enviado satisfactoriamente!</p>
            <button @click="closePopup" class="btn btn-secondary">Cerrar</button>
          </div>
        </form>
      <!-- <router-link to="/psicologos" class="btn psychologists-button">Lista de psicólogos</router-link> -->
      <button @click="viewWindow()" class="btn psychologists-button">Ir atrás</button>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
// import HTML_TEMPLATE from '../utils/messageMail'
// import SENDMAIL from "../utils/mail" 
import horariosPsico from '../utils/horariosPsico.json'

  export default {
    name: "Aggent",
    props: {
      "usernameLog": String,
      "usernameSend": String,
      "emailBegin": String,
      "emailSend": String,
    },
    data() {
      return {
        horariosPsico: {},

        emailObej: "",
        date: "",
        message: "",
        isFormValid: true,
        isEmailSent: false,
        showWindow: true,

        // check psicologos
        arrChecks: [],
        codigos: [],
        checkPsico: {
          index: 0,
          email: ""
        }

      };
    },

    async created() {
      await axios.get('http://127.0.0.1:8000/psychologist_schedule/all/details')
      .then(res => {
        this.horariosPsico = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.horariosPsico = JSON.parse(JSON.stringify(horariosPsico))
      });

      this.codigos = Object.keys(this.horariosPsico)
      this.arrChecks = Array(this.codigos.length).fill(false)
    },

    methods: {

      // selecciona un psicologo a citar
      toCheckPsico(psico_email, code) {
        if (this.arrChecks.some(elem => elem === true)) {
          const indexActive = this.arrChecks.findIndex(elem => elem === true);
          this.arrChecks[indexActive] = false
        }
        this.checkPsico.email = psico_email;
        this.checkPsico.index = this.codigos.indexOf(code);

        this.arrChecks[this.checkPsico.index] = true;
      },

      activeTr(code) {
        return {
          backgroundColor : (this.codigos.indexOf(code) === this.checkPsico.index)
                              ? "var(--color-feelscan-4)":""
        };
      },

      // funcion asincrona donde despues de enviar el correo, se confirme en el form
      async sendAggent(e) {
        if (this.date && this.message) {
          // Lógica para enviar el correo
          this.isFormValid = true;
          //implementar la lógica para enviar el correo

          // const options = {
          //     from:$props.emailBegin, // sender address
          //     to: $props.emailSend, // receiver email
          //     subject: "Reunion recomendada por FeelScan", // Subject line
          //     text: this.message,
          //     html: HTML_TEMPLATE(this.message),
          // }

          // SENDMAIL(options, (info) => {
          //   console.log("Email sent successfully");
          //   console.log("MESSAGE ID: ", info.messageId);
          // }
        } else {
          this.isFormValid = false; // El formulario no es válido
        }
      },
      closePopup() {
        this.isEmailSent = false;
      },

      viewWindow() {
        this.showWindow = false;
      }
    }
  }
</script>

<style scoped>

</style>