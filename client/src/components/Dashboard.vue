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
      viewEmotionEspec: false,

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
      countData: [],
      selectedOption: null,
      showtimeModal: false,
      
      // config main - psicologo
      configuracion: {},
      typeTochange: "",
      changed: "",

      top_limit: 20,
      rangeMainGraphic: 0,
      rangeFaceInfo: 0,

      exists_tenantId: true,
      
      chartOptions: {
        chart: {
          id: "line-chart",
        },
        xaxis: {
          categories: [], // lista para guardar los días que ponga
        },
      },
      chartData: [
        {
          name: "Emotion/Area Data",
          data: [],
        },
      ],
      emotion: "defaultEmotion",
      area: "defaultArea",
      days: 7, // Por default será una semana
  
    
    miembrosNoAtendidos: [],
     
    };
  },
  async created() {

    this.viewEmotionEspec = this.$props.role.includes("psico") || this.$props.role.includes("main")

      //// Obtener la configuracion general del dashboard
      await this.loadConfiguracion()
      
      //// si existe informacion de X institucion en el tenant_id muestra la informacion


    // ver el top negative emotions si eres main o spicologo
    if (this.viewEmotionEspec) {
      axios.get(`http://127.0.0.1:8000/member/all/top_negative`)
      .then(res => {
        this.puntajeMembers = res.data.content;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.puntajeMembers = JSON.parse(JSON.stringify(puntajes)) // por defecto si no esta activa
      });

    }
    
    // Obtener la emocion predominante
      this.getDominantEmotion();
      

    this.obtenerMiembrosNoAtendidos();

      //// peticion post que retorne la configuracion
      //// si existe informacion de X institucion en el tenant_id, se solicita al server la resp. informacion

      // Obtiene la lista de emociones que maneja nuestra data :p
      this.get('http://127.0.0.1:8000/emotion/all/names')
      .then(res => {
        this.emotionNames = res.data.content;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
      });

      // Obtener la cantidad de personas con la emocion predominante por area
      await axios.get(`http://127.0.0.1:8000/graphic/face-graphic?tenant_id=${this.$props.tid}`)
      .then(res => {
        this.circularEmotion = res.data.content;
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

    async loadConfiguracion() {
      await axios.get(`http://127.0.0.1:8000/configuracion/all`)
      .then(res => {
        this.configuracion = res.data.content;
      })
        .catch(error => {
          console.error('Error al obtener el dato:', error);
        });
    },

    getUserRow(index) {
      const infoUser = this.puntajeMembers[index-1]
      this.userToCitar = infoUser.nombre
      this.emailToCitar = infoUser.correo
    },

    async getDominantEmotion() {
      await axios.get('http://127.0.0.1:8000/emotion/predominant')
      .then(res => {
        this.dominantEmotion = res.data.content[0];
        this.countData = Object.keys(this.dominantEmotion);
        
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.dominantEmotion = "enojo"   // por defecto si no esta activa
      });

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

    fetchData(){
        const url = `http://127.0.0.1:8000/graphic/${this.emocion}/${this.area}/${this.dias}`;
        axios
        .get(url)
        .then((response) => {
          const newData = response.data; // Ajusta esto según el formato real de tus datos
          this.chartOptions.xaxis.area = newData.dates;
          this.chartData[0].data = newData.values;
        })

        .catch((error) => {
          console.error("Error fetching data:", error);
        });

    },

    changeEmotion(newEmotion){
      this.emocion = newEmotion;
      this.fetchData();
    },

    changeArea(newArea){
      this.area = newArea;
      this.fetchData();
    },

    changeTime(newTime){
      this.dias = newDays;
      this.fetchData();
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
    components: { Aggent, Teleport }
}

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
      <div><h1>Emocion dominante:</h1></div>
      <div id="get-dom-image">
          <span><em>{{ dominantEmotion }}</em></span>
          <img :src="`/${dominantEmotion}.jpg`" :alt="dominantEmotion" width="200">
      </div>  
    </div>
    

    <div id="circular-graph-b" class="box-info">
      <apexchart type="donut" :options="configPie" :series="countAreas"> </apexchart>
    </div>
    
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
  
  <div id="feature-emotion-trend-b" class="box-info" v-if="viewEmotionEspec">

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
  width: 100px;
  height: 70px;
  padding-right: 50px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

#get-dom-image span {
  padding-right: 30px;
  font-size: 20px;
}

#state-check {
  margin: 20px 23px 0 0;
}

#state-cell {
  display: flex;
  /* align-items: center; */
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
