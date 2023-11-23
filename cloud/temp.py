import csv
import boto3
from os import getenv

aws_access_key_id="ASIA6A6UW7LWVA4GUQ4E"
aws_secret_access_key="dxQ1Prv//cg/nfW1vlmIx/8y26uDHK7hHmVPJyIN"
aws_session_token="FwoGZXIvYXdzEPH//////////wEaDBxIV5zK9PUnKpdlqCLNAabJjGvOCsfJ4onK3FBtEvoP245WsA+QHmnSKBnc11GPGf5w3xwjNdWi7nw7ENOTSyOAgEndgR7DGFH5DzL7wbPbZakrfoPOaXuRxUEkxQJ5pFSebtkuXOMIWt3hO62BbaheA/LJVGrw3GWDInPsRwohf0lvuJEI9+IduJXETwE0XyF385Vju12em0jyLRODMqlAJhkiKhBy2MBEx60Od2ULoqZ6vdHUriI76tgOoY1ogTR6Oy1Cbzv10wM6KqMZyG9chKafHiWNxzsARpwogpr6qgYyLXsFtrSd3qtBEsfXHlhOUwLhxf1ligiwnynRf6No4oPPDjGa9OhvVoAl27uZ7Q=="
aws_region_name="us-east-1"

# Configura el cliente de DynamoDB
dynamodb_client = boto3.client('dynamodb',
         aws_access_key_id=aws_access_key_id,
         aws_secret_access_key=aws_secret_access_key,
         aws_session_token=aws_session_token,
         region_name=aws_region_name)



table_name = 't_emociones_miembros'

# Ruta del archivo CSV
csv_file_path = 'member_0.csv'

# Lee el archivo CSV y carga los datos a DynamoDB
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Convierte los tipos según sea necesario (puedes ajustar esto según tu esquema)
        item = {
            'tenant_id': {'S': 'UTEC'},
            'code': {'S': row['USER_ID']},
            'main_emotion': {'S': row['MAIN_EMOTION']}
        }
        print(item)

        # Añade el item a la tabla DynamoDB
        dynamodb_client.put_item(
            TableName=table_name,
            Item=item
        )

print(f'Datos importados a la tabla DynamoDB: {table_name}')
