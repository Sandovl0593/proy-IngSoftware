<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
    <title>"Registro de Asistencia"</title>
</head>
<body>
<div class="container">
    <h2>Registro de Asistencia</h2>
    <form id="myForm">
        <div class="form-group">
            <label for="codeInput">Validar Asistencia:</label>
            <input type="text" id="codeInput" placeholder="Ingrese su código" required>

        </div>

        <div class="form-group">
            <label for="numberSelect">Quiero conocer su opinión sobre la actividad:</label>
            <select id="numberSelect" required>
                <!-- Generar opciones del 1 al 20 -->
                //Emociones ,Rostros
                <script>
                    for (let i = 1; i <= 20; i++) {
                        document.write(`<option value="${i}">${i}</option>`);
                    }
                </script>
            </select>
        </div>

        <button type="button" onclick="addToTable()">Agregar a la tabla</button>
    </form>
</div>

<script src="script.js"></script>
</body>

</html>
