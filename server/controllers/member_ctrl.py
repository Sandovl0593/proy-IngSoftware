import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from fastapi.responses import JSONResponse
from database.db import dynamodb
from typing import Optional
from controllers.emotion_ctrl import get_emotion_predominant_member
from controllers.configuracion_ctrl import get_configuracion

table = 't_miembros'

def get_member(code: str, tenant_id = 'UTEC') -> Optional[dict]: ##
    try:
        response: dict = dynamodb.get_item(
            TableName=table,
            Key={
                'tenant_id': {'S': tenant_id}, 
                'code': {'S': code}
            },
        )
        
        item: dict = response.get('Item', {})

        member: dict = {
            'codigo': item.get('code', {}).get('S', ''),
            'nombre': item.get('nombre', {}).get('S', ''),
            'area': item.get('area', {}).get('S', ''),
            'puntaje': int(item.get('puntaje', {}).get('N', '0')),
            'correo': item.get('correo', {}).get('S', ''),
            'estado': int(item.get('estado', {}).get('N', '0'))
        }
        return member
        
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)


def update_member_state_score(code: str, state: int, tenant_id = 'UTEC') -> Optional[dict]: ##
    member: dict = get_member(code)
    current_score: int = int(member['puntaje'])
    new_score: int = calculate_new_score(current_score, state)

    try:    
        dynamodb.update_item(
            TableName=table,
            Key={
                'tenant_id': {'S': tenant_id}, 
                'code': {'S': code}
            },
            UpdateExpression='SET puntaje = :val1, estado = :val2',
            ExpressionAttributeValues={
                ':val1': {'N': str(new_score)},
                ':val2': {'N': str(state)}
            }
        )

        return {
            'mensaje': f'Puntuacion actualizada para miembro con codigo {code}. Nueva puntuación: {new_score})'
        }
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def actualizar_puntajes(tenant_id = 'UTEC'):
    tabla = dynamodb.Table(table)
    res = tabla.query(
        ProjectionExpression='code, nombre, area, puntaje, correo, estado',
        FilterExpression=(Key('tenant_id').eq(tenant_id))
    )
    miembros = res["Items"]
    for miembro in miembros:
        codigo = miembro.get('code', {}).get('S', '')
        estado = int(miembro.get('estado', {}).get('N', '0'))
        org = miembro.get('tenant_id', {}).get('S', '')
        update_member_state_score(codigo, estado, org)
    return {'mensaje': 'Puntajes actualizados'}


def get_members_top_negative(tenant_id = 'UTEC') -> Optional[dict]: ##
    
    try:
        members: list = []
        #obtener el limite 
        limit =  int(get_configuracion(tenant_id)['content']['lista'])

        response: dict = dynamodb.scan(
            TableName=table,
            ProjectionExpression='code, nombre, area, puntaje, correo',
            ExpressionAttributeNames={'#puntaje': 'puntaje', '#org': 'tenant_id'},
            ExpressionAttributeValues={':val1': {'N': '0'}, ':val2': {'S': tenant_id}},
            FilterExpression='(#puntaje >= :val1) AND (#org = :val2)'
        )
        items: dict = sorted(
            response['Items'], 
            key=lambda x: int(x['puntaje']['N']), 
            reverse=True
        )[:limit]
        
        for item in items:
            print(item)
            codigo = item.get('code', {}).get('S', '')
            emocion_predominante = get_emotion_predominant_member(codigo)
            member: dict = {
                'codigo': item.get('code', {}).get('S', ''),
                'nombre': item.get('nombre', {}).get('S', ''),
                'area': item.get('area', {}).get('S', ''),
                'puntaje': int(item.get('puntaje', {}).get('N', '0')),
                'correo': item.get('correo', {}).get('S', ''),
                'emocion_predominante': emocion_predominante['content']
            }
            members.append(member)
        return {'content': members}
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


# función para los nombres de los kmiembros (k < n = 20)
def obtener_miembros_no_atendidos(tenant_id='UTEC'):
    nombres = []
    tabla = dynamodb.Table(table)
    res = tabla.query(
        ProjectionExpression='nombre, estado',
        FilterExpression=(Key('estado').eq(0) & Key('tenant_id').eq(tenant_id)),
        Limit=20
    )
    items = res['Items']
    for item in items:
        no_atendido: dict = {
            'nombre': item.get('nombre', {}).get('S', ''),
        }
        nombres.append(no_atendido)
    return nombres


# modificar el estado (check = true, x = false)
def modificar_estado(check: bool, code: str, tenant_id='UTEC'):
    miembro: dict = get_member(code)
    estado_actual: int = int(miembro['estado'])
    if check:
        nuevo_estado = estado_actual + 1
    else:
        nuevo_estado = estado_actual - 1
    dynamodb.update_item(
        TableName=table,
        Key={
            'tenant_id': {'S': tenant_id},
            'code': {'S': code}
        },
        UpdateExpression='SET estado = :val',
        ExpressionAttributeValues={
            ':val': {'N': str(nuevo_estado)}
        }
    )
    return {
        'mensaje': f'Estado actualizado para miembro con codigo {code}. Nueva estado: {nuevo_estado})'
    }


# Auxiliary Functions


def calculate_new_score(current_score: int, state: int) -> int:
    return current_score - (20 if state == 1 else (50 if state == 2 else (100 if state == 3 else 0)))


convert_response = lambda response: {
    key: next(iter(value.values())) if isinstance(value, dict) else value for key, value in response.get('Item', {}).items()
}
