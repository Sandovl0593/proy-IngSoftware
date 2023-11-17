from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from database.db import dynamodb
from typing import Optional

table = 't_configuraciones'

def get_configuracion(tenant_id = 'UTEC')-> Optional[dict]:
    configuracion: dict = {}
    try:
        response: dict = dynamodb.scan(
            TableName=table,
            FilterExpression='tenant_id = :tenant_id',
            ExpressionAttributeValues={':tenant_id': {'S': tenant_id}}
        )
        for item in response['Items']:
            configuracion['main_graphic'] = item['main_graphic']['N']
            configuracion['lista'] = item['lista']['N']
            configuracion['face_graphic'] = item['face_graphic']['N']

        return {'content': configuracion}
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)

def update_configuracion(tipo: str, new_value: int, tenant_id = 'UTEC') -> Optional[dict]:
    try:
        if(tipo == 'list'):
            dynamodb.update_item(
                TableName=table,
                Key={
                    'tenant_id': {'S': tenant_id}, 
                },
                UpdateExpression='SET lista = :val1',
                ExpressionAttributeValues={
                    ':val1': {'N': str(new_value)},
                }
            )

        elif(tipo == 'face_graphic'):
            dynamodb.update_item(
                TableName=table,
                Key={
                    'tenant_id': {'S': tenant_id}, 
                },
                UpdateExpression='SET face_graphic = :val1',
                ExpressionAttributeValues={
                    ':val1': {'N': str(new_value)},
                }
            )  
        elif(tipo == 'main_graphic'):
            dynamodb.update_item(
                TableName=table,
                Key={
                    'tenant_id': {'S': tenant_id}, 
                },
                UpdateExpression='SET main_graphic = :val1',
                ExpressionAttributeValues={
                    ':val1': {'N': str(new_value)},
                }
            )
        else:  
            return { 'mensaje': f'Configuración no encontrada'}       

        return {
            'mensaje': f'Configuración actualiza para {tipo}. Nuevo valor: {new_value})'
        }
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)    

