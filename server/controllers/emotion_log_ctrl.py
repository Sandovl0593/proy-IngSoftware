from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from collections import defaultdict
from typing import Optional,List
from datetime import datetime

table = 't_registro_emociones'

def get_emotion_logs_member(member_code: str, from_date: str, tenant_id: str ='UTEC') -> Optional[dict]: ##
    formatted_from_date = f'{from_date}T00:00:00'
    try:
        response = dynamodb.scan(
            TableName=table,
            ProjectionExpression='emocion, code, fechaThora',
            ExpressionAttributeNames={'#fechaThora': 'fechaThora', '#tenant_id': 'tenant_id', '#code': 'code'},
            ExpressionAttributeValues={
                ':date': {'S': formatted_from_date},
                ':tenant_id': {'S': tenant_id},
                ':code': {'S': member_code}
            },
            FilterExpression='#fechaThora >= :date and #tenant_id = :tenant_id and #code = :code',
        )
        return response['Items']
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)


def get_emotion_logs(from_date: str, tenant_id: str ='UTEC') -> Optional[dict]: ##
    # example: 2023-03-20T08:25:00, from_date: 2023-03-20
    formatted_from_date = f'{from_date}T00:00:00'
    try:
        response = dynamodb.scan(
            TableName=table,
            ProjectionExpression='emocion, code, fechaThora',
            ExpressionAttributeNames={'#fechaThora': 'fechaThora', '#tenant_id': 'tenant_id'},
            ExpressionAttributeValues={
                ':date': {'S': formatted_from_date},
                ':tenant_id': {'S': tenant_id}
            },
            FilterExpression='#fechaThora >= :date and #tenant_id = :tenant_id',
        )
        return response['Items']
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)

#busca los registros en un rango de tiempo
def get_emotion_logs_range(start_date: str, end_date: str, tenant_id: str ='UTEC') -> Optional[List[dict]]:
    try:
        # Convertir las fechas de cadena a objetos datetime
        formatted_start_date = datetime.strptime(f'{start_date}T00:00:00', '%Y-%m-%dT%H:%M:%S')
        formatted_end_date = datetime.strptime(f'{end_date}T23:59:59', '%Y-%m-%dT%H:%M:%S')

        # Realizar la consulta a DynamoDB utilizando scan
        response = dynamodb.scan(
            TableName=table,  # Ajustar según tu configuración
            ProjectionExpression='emocion, code, fechaThora',
            ExpressionAttributeNames={'#fechaThora': 'fechaThora', '#tenant_id': 'tenant_id'},
            ExpressionAttributeValues={
                ':start_date': {'S': formatted_start_date.isoformat()},
                ':end_date': {'S': formatted_end_date.isoformat()},
                ':tenant_id': {'S': tenant_id}
            },
            FilterExpression='#fechaThora BETWEEN :start_date AND :end_date and #tenant_id = :tenant_id',
        )

        # Verificar si la clave 'Items' está presente en la respuesta
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error en la operación DynamoDB: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None


# Auxiliary Functions

def get_emotion_member_codes(items: dict) -> dict:
    emotions: defaultdict = defaultdict(list)
    for item in items:
        emotion: str = item['emocion']['S']
        code: str = item['code']['S']
        emotions[emotion].append(code)

    return dict(emotions) 

