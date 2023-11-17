<script>
import axios from 'axios'
import { Teleport } from 'vue'

import Aggent from './Aggent.vue'
import puntajes from '../utils/puntajes.json'
import emotionAreas from '../utils/emotion_areas.json'

export default {
  name: "Dashboard",

  props: {
    nameReg: String,
    emailReg: String,
    tid: String,
    role: String
  },
  data() {
    return {
      viewEmotionPsico: false,

      // state variables
      puntajeMembers: [],
      
      showAgent: false,
      unDoneCheck: [],
      meanWhileCheck: [],
      DoneCheck: [],

      dominantEmotion: "",
      imageDomEmotion: "",
      
      userToCitar: "",
      emailToCitar: "",

      current_date: "",
      mainGrafico: "",
      configPie: {},
      configLine: {},

      circularEmotion: {},
      serieAreas: [],
      countAreas: [],
      
      miembrosNoAtendidos: [],      
      top_limit: 20,     
    };
  },
  async created() {

    this.viewEmotionPsico = this.$props.role.includes("psico") || this.$props.role.includes("main")

    if (this.viewEmotionPsico) {
      await axios.get(`http://127.0.0.1:8000/member/all/top_negative/${this.top_limit}`)
      .then(res => {
        this.puntajeMembers = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.puntajeMembers = JSON.parse(JSON.stringify(puntajes)) // por defecto si no esta activa
        console.log(this.puntajeMembers)
      });
    }

    this.obtenerMiembrosNoAtendidos();
      //// peticion post que retorne la configuracion
      //// si existe informacion de X institucion en el tenant_id, se solicita al server la resp. informacion

      // Obtiene la lista de emociones que maneja nuestra data :p
      await this.get('http://127.0.0.1:8000/emotion/all/names')
      .then(res => {
        this.emotionNames = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
      });

      // Obtener la emocion predominante
      await this.getDominantEmotion();

      // Obtener la cantidad de personas con la emocion predominante por area
      await axios.get('http://127.0.0.1:8000/')
      .then(res => {
        this.circularEmotion = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.circularEmotion = JSON.parse(JSON.stringify(emotionAreas)) // por defecto si no esta activa
      });


      this.serieAreas = Object.keys(this.circularEmotion);
      this.countAreas = Object.values(this.circularEmotion);

      this.configPie = { 
        title: {
          text: "Porcentaje por área",
          align: "center",
        },
        chart: {
          width: '400px',
          height: '400px',
          zoom: {
            enabled: true
          },
          offsetY: 10
        },
        // Cambiar los colores
        colors: ['#BED346', '#E5D74C', '#E4B43D'],
        fill: {
          type: 'gradient',
        },
        labels: this.serieAreas,
        legend: {
          show: false
        }
      };
      
      // carga los estados checks de cada miembro por defecto
      for (let i = 0; i < this.puntajeMembers.length; i++) {
        this.unDoneCheck[i] = this.meanWhileCheck[i] = this.DoneCheck[i] = false;
      }
  },

  methods: {
    viewAgenda() {
      this.showAgent = !this.showAgent;
    },  

    getUserRow(index) {
      const infoUser = this.puntajeMembers[index-1]
      this.userToCitar = infoUser.nombre
      this.emailToCitar = infoUser.correo
    },

    async getDominantEmotion() {
      try {
    const response = await axios.get('http://127.0.0.1:8000/emotion/predominant');
    const responseData = response.data.content; // Obtenemos la lista de [emoción, porcentaje]
    
    if (responseData && responseData.length === 2) {
      const [emotion, percentage] = responseData;
      this.dominantEmotion = [emotion, percentage];
      this.countData = [emotion]; // Actualizamos countData solo con el nombre de la emoción
    } else {
      // Manejo de errores si la respuesta no tiene el formato esperado
      console.error('La respuesta del servidor no tiene el formato esperado.');
    }
  } catch (error) {
    console.error('Error al obtener el dato:', error);
    this.dominantEmotion = ["enojo", 0]; // Valores predeterminados si hay un error
    this.countData = ["enojo"];
  }

  this.updateChart();
    },

    async obtenerMiembrosNoAtendidos() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/obtener_miembros_no_atendidos');
        this.miembrosNoAtendidos = response.data; // Actualiza la variable con la lista recibida del servidor
      } catch (error) {
        console.error('Error al obtener la lista de miembros no atendidos:', error);
      }
    }, 
    // funciones asincronas sibre actualizar el puntaje
    // en .then() ocurre si funciona la peticion PUT

    async tounDoneCheck(index) {
      if (this.unDoneCheck[index]) {
        await axios.put(`http://127.0.0.1:8000/member/${codeuser}/state/cambiar/1`).then(
          res => {
            this.meanWhileCheck[index] = false;
            this.DoneCheck[index] = false;
          }
        )
      }
      const codeuser = this.puntajeMembers[index-1].codigo
      await axios.put(`http://127.0.0.1:8000/member/${codeuser}/state/1/score`)
      .then(res => this.puntajeMembers[index-1].puntaje -= 20) //
    },
    
    async toNeanwhileCheck(index) {
      if (this.meanWhileCheck[index]) {
        await axios.put(`http://127.0.0.1:8000/member/${codeuser}/state/cambiar/2`).then(
          res => {
            this.unDoneCheck[index] = false;
            this.DoneCheck[index] = false;
          }
        )
      }
      const codeuser = this.puntajeMembers[index-1].codigo
      await axios.put(`http://127.0.0.1:8000/member/${codeuser}/state/2/score`) //
      .then(res => this.puntajeMembers[index-1].puntaje -= 50) //
      
    },
    
    async toDoneCheck(index) {
      if (this.DoneCheck[index]) {
        await axios.put(`http://127.0.0.1:8000/member/${codeuser}/state/cambiar/3`).then(
          res => {
            this.unDoneCheck[index] = false;
            this.meanWhileCheck[index] = false;
          }
        )
      }
      const codeuser = this.puntajeMembers[index-1].codigo
      await axios.put(`http://127.0.0.1:8000/member/${codeuser}/state/3/score`) //
      .then(res => this.puntajeMembers[index-1].puntaje -= 100) //
    }
  },
  components: { Aggent, Teleport}

</script>

<template>

<section>
  
  <div id="select-emotion-b" class="box-info">

    <div id="pet-select-em"><h4>Selecciona la emoción: </h4></div>
    <div id="form-select-em">
      <form action="#">
        <label for="select-emotion">
          <select name="emotion-active" id="lang">
            <option value="felicidad">Felicidad</option>
            <option value="tristeza">Tristeza</option>
            <option value="estres">Estres</option>
            <option value="enojo">Enojo</option>
            <option value="ansiedad">Ansiedad</option>
            <option value="aburrimiento">Aburrimiento</option>
            <option value="alivio">Alivio</option>
          </select>
        </label>
      </form>
    </div>

  </div>
  

  <div id="section-emotion">

    <div id="dominant-emotion-b" class="box-info">
      <div>
        <h1>Emoción dominante:</h1>
        <p>Porcentaje: {{ dominantEmotion[1] }}%</p>
      </div>
      <div id="get-dom-image">
        <span><em>{{ dominantEmotion[0] }}</em></span>
        <img :src="`/${dominantEmotion[0]}.jpg`" :alt="dominantEmotion[0]" width="150">
      </div>
    </div>
    

    <div id="circular-graph-b" class="box-info">
      <apexchart type="donut" :options="configPie" :series="countAreas"> </apexchart>
    </div>
    
  </div>

 <div id="miembros-no-atendidos-b" class="box-info">
      <h3 style="color: black;">Miembros no atendidos</h3>
      <ul>
        <li v-for="(miembro, index) in miembrosNoAtendidos" :key="index">
          {{ miembro.nombre }}
        </li>
      </ul>
    </div>
  
  <div id="chart-emotion-area-b" class="box-info">
    <div class = "chart-buttons">
      <button @click="selectOption('emotion')">Felicidad</button>
      <button @click="selectOption('area')">Ciencias</button>
      <button @click="selectOption('timeRank')">1 semana</button>
    </div>

    <div id="chart-info">
      <apexchart type="line" :options="chartOptions" :series="chartData"></apexchart>
    </div>
    
<!-- Hice un modal para cuando seleccionen el rango de tiempo, algo así como lo de las notificaciones -->

    <!-- <Teleport to="#chart-emotion-area-b"> -->
      <div class="timeModal" v-if="showtimeModal">
        <div class="modal-content">
          <span class="close" @click="closetimeModal">&times;</span>
          <label for="timeSelect">Rango de Tiempo:</label>
          <select id="timeSelect" v-model="selectedtime">
            <option value="1d">1 día</option>
            <option value="1w">1 semana</option>
            <option value="2w">2 semanas</option>
            <option value="1m">1 mes</option>
          </select>
          <button @click="handleTimeSelection">Aceptar</button>
        </div>
      </div>
    <!-- </Teleport> -->

  </div>
  
  <div id="feature-emotion-trend-b" class="box-info" v-if="viewEmotionPsico">

    <div id="scroll-block">
      <div id="table-box">
        <table id="miembros-table">
        <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th><th>Área</th>
              <th>Puntaje</th>
              <th>Asistencia</th>
            </tr>
        </thead>
        <tbody>
          <!-- Los datos se cargan EN VUE -->
          <tr :id="`row-${index++}`" v-for="(row, index) in puntajeMembers" :key="index">
            <td> {{ row.codigo }} </td>
            <td> {{ row.nombre }} </td>
            <td> {{ row.area }} </td>
            <td> {{ row.puntaje }} </td>
            <td id="state-cell">
              <div id="state-check">
                <input type="checkbox" class="check-style n-undone" v-model="unDoneCheck[index]" @change="tounDoneCheck(index)">
                <input type="checkbox" class="check-style n-meanwhile" v-model="meanWhileCheck[index]" @change="toNeanwhileCheck(index)">
                <input type="checkbox" class="check-style n-done" v-model="DoneCheck[index]" @change="toDoneCheck(index)">
              </div>
            </td>
          </tr>
            
          </tbody>
        </table>
      </div>
    
      <div id="agent-button">
        <h5>Citar</h5>
          <div :id="`li-${index-1}`" v-for="index in puntajeMembers.length" :key="index">
            <div id="plus-env" @click="{getUserRow(index); viewAgenda()}"><h1>+</h1></div>
          </div>
      </div>

    </div>
    

  </div>

</section>


<Aggent v-if="showAgent" :usernameLog="$props.nameReg" :emailBegin="$props.emailReg" 
                         :usernameSend="userToCitar" :emailSend="emailToCitar"/>


</template>

<style scoped>
#get-dom-image {
  width: 500px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: transparent;
}

#dominant-emotion-b img {
  margin-top: 20px; 
  width: 500px;
  height: auto; 
}

#get-dom-image span {
  padding-right: 30px;
  font-size: 20px;
  background: transparent;
  margin-top: 50px; 
}

#state-check {
  margin: 20px 23px 0 0;
}

#state-cell {
  display: flex;
  width: 80%;
}

.check-style {
    margin-left: 5px;
    cursor: pointer;
}

.n-undone:checked { 
  accent-color: red;
} 

.n-meanwhile:checked { 
    accent-color: yellow; 
} 

.n-done:checked { 
    accent-color: #2BAF6B; 
}

.chart-buttons{
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.timeModal{
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: #fefefe;
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  z-index: 99;
  border: 1px solid #888;
  width: 80%;
  border-radius: 10px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

#timeSelect {
  margin-right: 10px;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.chart-buttons button {
  padding: 8px;
  background-color: #377c39;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.chart-buttons button:hover {
 opacity: 2.9;
}

#miembros-no-atendidos-b {
  border-radius: 10px;
  box-shadow: 2px 3px 3px 0 black;
  background-color: var(--color-feelscan-4);
  border: 0.1px solid orange;
  margin-bottom: 35px;
  padding: 20px;
}

#miembros-no-atendidos-b h3 {
  color: var(--color-feelscan-2);
  margin-bottom: 15px;
}

#miembros-no-atendidos-b ul {
  list-style: none;
  padding: 0;
}

#miembros-no-atendidos-b li {
  margin-bottom: 10px;
  color: #555;
}






</style>
