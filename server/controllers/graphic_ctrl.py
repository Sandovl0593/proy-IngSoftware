from controllers.emotion_log_ctrl import get_emotion_logs, get_emotion_member_codes
from controllers.member_ctrl import get_member
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Optional

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
