<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Correo electrónico</title>
  <script src="https://cdn.jsdelivr.net/npm/vue@2"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css">
</head>
<body>
<div id="app" class="container is-primary">
  <button class="button is-primary" @click="openModal">Enviar correo</button>
  <button class="button is-info" @click="openSchedule">Ver Horario</button>
  <modal :is-active="modalActive" @close="closeModal"></modal>
  <schedule-modal :is-active="scheduleActive" @close="closeSchedule"></schedule-modal>
</div>

<script>
  Vue.component('modal', {
    template: `
            <div class="modal" :class="{ 'is-active': isActive }">
                <div class="modal-background" @click="$emit('close')"></div>
                <div class="modal-content">
                    <div class="box">
                        <h2 class="title is-5">Enviar correo electrónico</h2>
                        <form @submit.prevent="submitForm">
                            <div class="field">
                                <label class="label">Para</label>
                                <div class="control">
                                    <input v-model="email" class="input" type="email" placeholder="Correo electrónico" required>
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Asunto</label>
                                <div class="control">
                                    <input v-model="subject" class="input" type="text" placeholder="Asunto" required>
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Mensaje</label>
                                <div class="control">
                                    <textarea v-model="message" class="textarea" placeholder="Mensaje" required></textarea>
                                </div>
                            </div>
                            <div class="field is-grouped">
                                <div class="control">
                                    <button type="submit" class="button is-link">Enviar</button>
                                </div>
                                <div class="control">
                                    <button class="button is-link is-light" @click="$emit('close')">Cancelar</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <button class="modal-close is-large" aria-label="close" @click="$emit('close')"></button>
            </div>
        `,
    props: ['isActive'],
    data() {
      return {
        email: '',
        subject: '',
        message: ''
      };
    },
    methods: {
      submitForm() {

        console.log('Correo enviado a:', this.email, 'con asunto:', this.subject, 'y mensaje:', this.message);

        this.$emit('close');
      }
    }
  });

  Vue.component('schedule-modal', {
    template: `
            <div class="modal" :class="{ 'is-active': isActive }">
                <div class="modal-background" @click="$emit('close')"></div>
                <div class="modal-content">
                    <div class="box">
                        <h2 class="title is-5">Horario de Psicólogos</h2>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Día</th>
                                    <th>Horario</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(day, schedule) in scheduleData" :key="day">
                                    <td>{{ day }}</td>
                                    <td>{{ schedule }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <button class="modal-close is-large" aria-label="close" @click="$emit('close')"></button>
            </div>
        `,
    props: ['isActive'],
    data() {
      return {
        scheduleData: {
          'Lunes': '9:00 AM - 5:00 PM',
          'Martes': '10:00 AM - 6:00 PM',
        }
      };
    }
  });

  new Vue({
    el: '#app',
    data() {
      return {
        modalActive: false,
        scheduleActive: false
      }
    },
    methods: {
      openModal() {
        this.modalActive = true;
      },
      closeModal() {
        this.modalActive = false;
      },
      openSchedule() {
        this.scheduleActive = true;
      },
      closeSchedule() {
        this.scheduleActive = false;
      }
    }
  });
</script>
</body>
</html>
