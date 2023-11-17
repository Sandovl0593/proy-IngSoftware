from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Optional
from database.db import dynamodb
import json

table = 't_graficos'


#Obtener la ultima fecha t_registro_emociones 
def get_last_date(tenant_id: str ='UTEC'):
    try:
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

        if 'Items' in response and len(response['Items']) > 0:
            return {'content': response['Items'][0]['fechaThora_emocion_area']['S']}
        else:
            return JSONResponse(content={"error": "No hay elementos para este tenant_id"}, status_code=404)

    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)        

def get_data_main_graphic(dias: int = 1, emocion: str ='tristeza', area: str ='Bienestar Estudiantil', tenant_id: str ='UTEC')-> Optional[dict]:
    try:
        #Obtener la fecha 
        ultimaFecha = get_last_date(tenant_id)['content'].split('T')[0]

        fecha_limite = datetime.strptime(ultimaFecha[:19], "%Y-%m-%d")
        fecha_limite -= timedelta(days=dias)

        fecha_limite_str = fecha_limite.strftime("%Y-%m-%dT%H:%M:%S")

        #Prueba
        fechaLimite = str(fecha_limite_str) + '-alivio-Administracion y Finanzas' 

        # Expresión de condición
        condition_expression = "tenant_id = :tenant_id AND fechaThora_emocion_area > :fechaLimite"

        # Atributos de expresión
        expression_attribute_values = {
            ':tenant_id': {'S': tenant_id},
            ':fechaLimite': {'S': fechaLimite}
        }

        # Realizar la consulta
        response = dynamodb.query(
            TableName=table,
            KeyConditionExpression=condition_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

        valores = {}
        for item in response['Items']:
            fechaThora_emocion_area: str = item['fechaThora_emocion_area']['S']
            fechaThora = fechaThora_emocion_area[:19]
            temp = fechaThora_emocion_area.split('-')
            if(temp[3] == emocion and temp[4] == area): 
                count = int(item['count']['N'])
                valores[fechaThora] : int = count

        return {'content': valores}
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)


''' 
def get_values_main_graphic(from_date: datetime = datetime(2023, 8, 20), tenant_id: str = 'UTEC') -> Optional[dict]:
    try:
        timestamp_list: list = get_x_main_graphic(from_date)
        # format: str = '%Y-%m-%dT%H:%M:%S'
        values: dict = get_emotion_logs(from_date, tenant_id) # todos los valores sin filtrar por area o emocion 
        # Inicializa un diccionario vacío
        date_dict: dict = {key: 0 for key in timestamp_list}

        for date_list in timestamp_list:
            for item in values:
                if item['fechaThora']['S'] <= date_list and item['fechaThora']['S'] >= str(from_date):
                    date_dict[date_list] += 1
        return date_dict 
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)


def get_emotion_area_members_graphic(from_date: str, emotion: str = 'tristeza', area: str = 'Computer Science', tenant_id: str = 'UTEC'):
    from_date: str = f'{from_date}T00:00:00'
    codes_members_select: list = []
    try:
        items: dict = get_emotion_logs(from_date, tenant_id)
        emotion_codes: dict = get_emotion_member_codes(items)
        # total ids que estan <emocion> en el intervalo de tiempo
        codes_current_emotion: list = emotion_codes[emotion] 
        for code in codes_current_emotion:
            member: dict = get_member(code, tenant_id)
            area_member: str = member['area']
            if area_member == area:
                codes_members_select.append(code)

        return {'content': codes_members_select}
    except ClientError as e:
            return JSONResponse(content=e.response['Error'], status_code=500)
    
#retorna los codigos de las personas que tienen la emocion predominante y en una area dato un rango de tiempo
def get_emotion_area_members_rage_time(from_date: str,to_date: str, emotion: str = 'tristeza', area: str = 'Computer Science', tenant_id: str = 'UTEC'):

    codes_members_select: list = []
    try:
        items: dict = get_emotion_logs_range(from_date,to_date, tenant_id)
        emotion_codes: dict = get_emotion_member_codes(items)
        # total ids que estan <emocion> en el intervalo de tiempo
        codes_current_emotion: list = emotion_codes[emotion] 
        for code in codes_current_emotion:
            member: dict = get_member(code, tenant_id)
            area_member: str = member['area']
            if area_member == area:
                codes_members_select.append(code)

        return {'content': codes_members_select}
    except ClientError as e:
            return JSONResponse(content=e.response['Error'], status_code=500)
    
#funcion que cuenta cuantas personas de cada area tienen la emocion predominante en unrango de dias
def cont_emotionpred_area(end_date: str,cant_dias:int):
    area_emotionpred={}
    emotion_pred= get_emotion_predominant()['content']
    areas= get_areas('UTEC')['content']
    # Convertir end_date a objeto datetime
    fin_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    # Restar cant_dias a fin_date_obj
    inicio_date_obj = fin_date_obj - timedelta(days=cant_dias)
    for area in areas:
        # Utilizar fechas como cadenas en la llamada a la función
        code=get_emotion_area_members_rage_time(inicio_date_obj.strftime("%Y-%m-%d"),fin_date_obj.strftime("%Y-%m-%d"), emotion_pred, area, 'UTEC')
        area_emotionpred[area] = len(code['content'])
    json_content = json.dumps(area_emotionpred, indent=4)
    with open('emotion_areas.json', 'w') as json_file:
        json.dump(area_emotionpred, json_file, indent=4)
    return json_content

# Auxiliary Functions

def get_x_main_graphic(from_date: datetime = datetime(2023, 8, 20, 0,0,0)) -> list:
    end_date: datetime = datetime(2023, 8, 28, 0,0,0)
    timestamp_list: list = []
    current_date: datetime = from_date

    while current_date <= end_date:
        # Verificar si la hora actual está entre las 6 AM (6) y las 11 PM (23)
        if 6 <= current_date.hour <= 23:
            timestamp_list.append(current_date.strftime('%Y-%m-%dT%H:%M:%S'))
        current_date += timedelta(hours=3)
    return timestamp_list
#cont_emotionpred_area("2023-08-22",2)'''