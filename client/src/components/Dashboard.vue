<script>
import axios from 'axios'
import { Teleport } from 'vue'
import Aggent from './Aggent.vue'
import puntajes from '../utils/puntajes.json'

export default {
  name: "Dashboard",
  data() {
    return {
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
      circularEmotion: "",

      top_limit: 20,

      // showNotifications: true,
      // citasPendientes: ["Margiory", "Marcela", "Milloshy", "Fabiola", "Adrian"],
     
    }
  },
  created() {
      // axios.get(`http://127.0.0.1:8000/graphic/main/member_codes/${this.current_date}/${this.circularEmotion}/`)
      // .then(res => {
      //   this.mainGrafico = res.data;
      // })
      // .catch(error => {
      //   console.error('Error al obtener el dato:', error);
      // });
      
      axios.get(`http://127.0.0.1:5000/member/all/top_negative/${this.top_limit}`)
      .then(res => {
        this.puntajeMembers = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.puntajeMembers = JSON.parse(JSON.stringify(puntajes))
      });

      axios.get('http://127.0.0.1:5000/emotion/predominant')
      .then(res => {
        this.dominantEmotion = res.data;
      })
      .catch(error => {
        console.error('Error al obtener el dato:', error);
        this.dominantEmotion = "enojo"   // por defecto si no esta activa
      });
      
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
          <img :src="`./public/images/` + dominantEmotion + '.jpg'" :alt="dominantEmotion" width="100">
      </div>  
    </div>
    

    <div id="circular-graph-b" class="box-info">
      
    </div>
    
  </div>
  

  <div id="chart-emotion-area-b" z>
    {{ mainGrafico }}
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
                <input type="checkbox" :class="`check-style n-undone`" v-model="unDoneCheck[index]" @change="tounDoneCheck(index)">
                <input type="checkbox" :class="`check-style n-meanwhile`" v-model="meanWhileCheck[index]" @change="toNeanwhileCheck(index)">
                <input type="checkbox" :class="`check-style n-done`" v-model="DoneCheck[index]" @change="toDoneCheck(index)">
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

<Aggent v-if="showAgent" :username="userToCitar" :email="emailToCitar"/>


</template>

<style scoped>

#get-dom-image {
  width: 100px;
  padding-top: 30px;
  height: 70px;
  display: flex;
  align-items: center;
  vertical-align: middle;
  justify-content: space-around;
  /* border: 1px solid black; */
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
    accent-color: green; 
} 

</style>
