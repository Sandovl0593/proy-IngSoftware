from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from collections import defaultdict
from typing import Optional,List
from datetime import datetime
from datetime import datetime, timedelta
from controllers.configuracion_ctrl import get_lista_days

table = 't_registro_emociones'
table2 = 't_miembros'
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
def get_last_date(tenant_id: str ='UTEC'):

    query_expression = (
        "tenant_id = :tenant_id"
    )

    expression_attribute_values = {':tenant_id': {'S': tenant_id}}

    response = dynamodb.query(
        TableName=table,
        KeyConditionExpression=query_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ScanIndexForward=False, 
        Limit=1 
    )

    return(response['Items'][0]['fechaThora']['S'].split('T')[0])
     


def refresh_puntaje(tenant_id='UTEC'):
    emociones_puntajes = {
    'tristeza': 10,
    'estres': 4,
    'ansiedad': 5,
    'frustracion': 5,
    'enojo': 8,
    'aburrimiento': 2,
    'preocupacion': 3,
    'motivacion': -5,
    'felicidad': -10,
    'satisfaccion': -4,
    'alivio': -2
    }
    datos_puntajes = {}
    fecha=get_last_date(tenant_id)
    #fecha="2023-08-22"
    cant_dias=get_lista_days(tenant_id)
    fin_date_obj = datetime.strptime(fecha, "%Y-%m-%d")
    inicio_date_obj = fin_date_obj - timedelta(days=cant_dias)
    print(inicio_date_obj)
    registros=get_emotion_logs_range(inicio_date_obj.strftime("%Y-%m-%d"),fin_date_obj.strftime("%Y-%m-%d"),'UTEC')
    for registro in registros:
        codigo=registro['code']['S']
        emocion=registro['emocion']['S']

        puntaje = emociones_puntajes.get(emocion, 0)
        if codigo in datos_puntajes:
            datos_puntajes[codigo] += puntaje
        else:
            datos_puntajes[codigo] = puntaje
    
    #actualizar el puntaje 
    for item in datos_puntajes:
        #update_member_puntaje(item, datos_puntajes[item],tenant_id)
        dynamodb.update_item(
        TableName=table2,
        Key={
            'tenant_id': {'S': tenant_id}, 
            'code': {'S': item}
        },
        UpdateExpression='SET puntaje = :val1',
        ExpressionAttributeValues={
            ':val1': {'N': str(datos_puntajes[item])},
        }    
    )

    return "datos actualizado exitosamente"

