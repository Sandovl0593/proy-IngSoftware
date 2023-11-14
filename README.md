<a name="readme-top"></a>

<div align="center">
  <img align="center" src="images/logo.jpg" width="100"/>
  <a href="https://github.com/Sandovl0593/proy-IngSoftware">
  </a>
  <h1>💚 <em>FeelScan</em> 💚</h1>
</div>

<h4 align="center"><em>Sistema de recomendación (IA) de actividades
a realizar en base a las estadísticas de las emociones de los miembros en una institución, brindándole un soporte al personal o área encargada de salud mental</em></h4>
<h5 align="center"><em>Producto desarrollado en el curso de Ing. de Software - Computer Science</em></h5>

<details open>
  <summary><h2>&nbsp Contents</h2></summary>
  <ul>
    <li><a href="#team">Team</a></li>
    <li><a href="#user">User</a></li>
    <li><a href="#pain-points">Pain Points</a></li>
    <li><a href="#database">Database</a></li>
    <li><a href="#development">Development</a></li>
    <li><a href="#views">Views</a></li>
    <li><a href="#deployment">Deployment</a></li>
    <li><a href="#annexes">Annexes</a></li>
  </ul>
</details>


## Team 

<div align="center">

|    1    |    2    |    3    |    4    |    5    |    6    |    7    |   8   |
|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
**Back-end**|**Back-end**|**Front-end**|**Front-end**|**Back-end**|**Front-end**|**Front-end**|**Back-end**|
|Marcela <br>Espinoza <br>Herrera|Kelvin<br>Cahuana<br>Condori|Adrian<br>Sandoval<br>Huamaní|Margiory<br>Alvarado<br>Chávez|Milloshy <br>Crisóstomo<br>Rodríguez|Fabián<br> Alvarado <br> Vargas|Fabiola<br>Guardamino<br>Morales|José <br>Osnayo <br> Matos

</div>


## User

Área encargada de salud y bienestar que proporcionan actividades y seguimientos psicilógicos a los miembros de una institución.

## Pain Points

|||
|--|--|
1.|No saber qué alumnos priorizar para su atención psicológica. A mayor cantidad de estudiantes, mayor es la dificultad de atención para todos. Puesto que las reservas para estas citas se agotan en las primeras semanas de clases.
2.|En caso exista un bajo rendimiento académico de un estudiante está asociado con un problema emocional (salud mental, motivación, etc.) o tenga otro tipo de dificultades que no es muy aentrado a la sociabilidad o autoconfianza con déficits de salud.
3.|Los estudiantes pocos sociables para integrarlos a las actividades de la universidad con distintos tipos de talleres que sean efectivos para el desarrollo de esa emoción
4.|Los estudiantes que no responden las encuestas que realiza bienestar estudiantil para saber la condición de los estudiantes en determinado tiempopor cuestión de tiempo o vergüenza.

## Development

### _Mock Data_

- Generados en Python con `Faker` y `random` guardados como CSV en `server/data`
- Datos previos de fetching en `/client/src/utils/`

### _Database_

- Utilizando Amazon DynamoDB de estilo Multitenancy con `"tenant_id": "UTEC"` (usuario predeterminado)
- Modelado de Datos con `pydantic` y `typing` para instanciar las tablas

### _Environment_

- **Back-end** con `FastAPI` localmente

```bash
cd server
pip3 install -r requirements.txt
uvicorn main:app --reload --env-file=".env"  # .env : las credenciales de AWS
```

- **Front-end** con `npm` o `pnpm` en modo desarrollo

```bash
cd client
npm install
npm run dev
```

### _Arquitecture_

## Views

- **`/dashboard`**: Contiene el reporte de las emociones predominantes en un periodo específico, gráficos estadísticos de las emociones por área resumidas y el listado de las personas por prioridad de recibir recomendaciones.

- **`/recommendation`**: 

- **`/profile`**:

## Deployment

[ despliegue de la plataforma web ]

## Annexes

### [Prototype](https://app.moqups.com/L4DOzpgZmVrPYT0dtXQNG5a2IRYaGvHz/edit/page/ade76401d)

|<img src="images/dashboard.png" width="800"/> | <img src="images/search.png" width="800"/> | <img src="images/userview.png" width="800"/> |
|-|-|-|

### Class diagram

<div align="center">
  <img src="images/classes_diag.png" width="600"/>
</div>

<hr>

### Contributing

<div align="center">

![Alt](https://repobeats.axiom.co/api/embed/8345d369ea8e3eab3bbabaad467545ecd6303c62.svg "Repobeats analytics image")

</div><hr>

<p align="right"><a href="#top">Back to top 🔼</a></p>
