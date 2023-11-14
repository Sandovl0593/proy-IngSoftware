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
    emailReg: String
  },
  data() {
    return {
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

      circularEmotion: "",
      serieAreas: [],
      countAreas: [],
      countData: [],

      top_limit: 20,
     
    }
  },
  async created() {

      // Obtener los miembros por puntaje en orden descendente
      await axios.get(`http://127.0.0.1:8000/member/all/top_negative/${this.top_limit}`)
      .then(res => {
        this.puntajeMembers = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.puntajeMembers = JSON.parse(JSON.stringify(puntajes)) // por defecto si no esta activa
      });
      
      // Obtener las coordenadas del grafico dependienedo de la emocion y el rango de tiempo
      // axios.get(`http://127.0.0.1:8000/graphic/main/member_codes/${this.current_date}/${this.circularEmotion}/`)
      // .then(res => {
      //   this.mainGrafico = res.data;
      // })
      // .catch(error => {
      //   console.error('Error al obtener el dato:', error);
      // });

      // Obtener la emocion predominante
      await axios.get('http://127.0.0.1:8000/emotion/predominant')
      .then(res => {
        this.dominantEmotion = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.dominantEmotion = "enojo"   // por defecto si no esta activa
      });

      // Obtener la cantidad de personas con la emocion predominante por area
      await axios.get('http://127.0.0.1:8000/--')
      .then(res => {
        this.circularEmotion = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.circularEmotion = JSON.parse(JSON.stringify(emotionAreas)) // por defecto si no esta activa
      });


      this.serieAreas = Object.keys(this.circularEmotion);
      this.countAreas = Object.values(this.circularEmotion);
      this.countData = Object.keys(this.dominantEmotion);

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
          // position: 'bottom',
          // width: '340px',
          // height: '200px',
          // fontSize: '10px',
          // offsetX: 10,
          // offsetY: 10,
          // formatter: (series, opts) => [this.serieAreas[opts.seriesIndex]]
        }
      };

      this.configLine = { 
        title: {
          text: "Visualización de Data por rango seleccionado",
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
        colors: ['#d6c43e', '#cdcd32', '#d6a751'],
        fill: {
          type: 'gradient',
        },
        labels: this.serieData,
        legend: {
          show: true
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

    // funciones asincronas sibre actualizar el puntaje
    // en .then() ocurre si funciona la peticion POST

    async tounDoneCheck(index) {
      if (this.unDoneCheck[index]) {
        this.meanWhileCheck[index] = false;
        this.DoneCheck[index] = false;
      }
      const codeuser = this.puntajeMembers[index-1].codigo
      await axios.post(`http://127.0.0.1:8000/member/${codeuser}/state/1/score`)
      .then(res => this.puntajeMembers[index-1].puntaje -= 20) //
    },
    
    async toNeanwhileCheck(index) {
      if (this.meanWhileCheck[index]) {
        this.unDoneCheck[index] = false;
        this.DoneCheck[index] = false;
      }
      const codeuser = this.puntajeMembers[index-1].codigo
      await axios.post(`http://127.0.0.1:8000/member/${codeuser}/state/2/score`) //
      .then(res => this.puntajeMembers[index-1].puntaje -= 50) //
      
    },

    async toDoneCheck(index) {
      if (this.DoneCheck[index]) {
        this.unDoneCheck[index] = false;
        this.meanWhileCheck[index] = false;
      }
      const codeuser = this.puntajeMembers[index-1].codigo
      await axios.put(`http://127.0.0.1:8000/member/${codeuser}/state/3/score`) //
      .then(res => this.puntajeMembers[index-1].puntaje -= 100) //
    },
  },

  mounted() {

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
          <img :src="`/${dominantEmotion}.jpg`" :alt="dominantEmotion" width="100">
      </div>  
    </div>
    

    <div id="circular-graph-b" class="box-info">
      <apexchart type="donut" :options="configPie" :series="countAreas"> </apexchart>
    </div>
    
  </div>
  

  <div id="chart-emotion-area-b" class="box-info">
    <apexchart type="line" :options="configLine" :series="countData"></apexchart>
  </div>
  
  <div id="feature-emotion-trend-b" class="box-info">

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

</style>
