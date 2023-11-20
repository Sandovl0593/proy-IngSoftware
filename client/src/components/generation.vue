<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de QR</title>
    <!-- Incluye la librería qrcode.min.js desde un CDN -->
    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.4.4/dist/qrcode.min.js"></script>
</head>
<body>
<h1>Escanee QR</h1>

<!-- Input para ingresar el texto del QR -->
<label for="qr-text">Texto para el QR:</label>
<input type="text" id="qr-text" placeholder="Emociones">

<!-- Botón para generar el QR -->
<button onclick="generateQR()">Generar QR</button>
<img>

<!-- Contenedor donde se mostrará el QR -->
<div id="qrcode"></div>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Página con QR</title>
</head>
<body>

<!-- Contenedor del QR -->
<div id="qr-container">
    <img src="URL_DE_TU_IMAGEN_QR" alt="Código QR">
</div>

</body>
</html>



<script>
    // Función para generar el QR
    function generateQR() {

        // Obtiene el texto ingresado
        var qrText = document.getElementById("qr-text").value;

        // Seleccion del contenedor donde se mostrará el QR
        var qrContainer = document.getElementById("qrcode");

        var qrcode = new QRCode(qrContainer, {
            text: qrText,
            width: 128,
            height: 128
        }
    });
    }
</script>
</body>
</html>
