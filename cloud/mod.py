import csv

# Nombre del archivo de entrada y salida
input_filename = 'updated_activities.csv'
output_filename = './data/activity_0.csv'

# Columnas que deseas incluir en el archivo de salida
columnas_a_incluir = ['activity_id', 'name', 'emotion']

# Abrir el archivo de entrada en modo lectura
with open(input_filename, 'r') as input_file:
    # Crear un lector CSV
    csvreader = csv.DictReader(input_file)

    # Extraer las filas del archivo de entrada
    filas = list(csvreader)

# Filtrar las columnas que deseas mantener
filas_filtradas = []
for fila in filas:
    fila_filtrada = {columna: fila[columna] for columna in columnas_a_incluir}
    filas_filtradas.append(fila_filtrada)

# Abrir el archivo de salida en modo escritura
with open(output_filename, 'w', newline='') as output_file:
    # Definir las columnas del archivo de salida
    fieldnames = columnas_a_incluir

    # Crear un escritor CSV
    csvwriter = csv.DictWriter(output_file, fieldnames=fieldnames)

    # Escribir las filas filtradas en el archivo de salida
    csvwriter.writeheader()
    csvwriter.writerows(filas_filtradas)

print(f'Se han filtrado las columnas y el resultado se ha guardado en {output_filename}.')
