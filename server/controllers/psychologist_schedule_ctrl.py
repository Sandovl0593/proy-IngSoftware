from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from controllers.member_ctrl import get_member
from database.db import dynamodb
from typing import Optional
import ast

table = 't_horario_psicologos'

def get_psychologist_schedules_details(tenant_id ='UTEC') -> Optional[dict]: ##
    try:
        response: dict = dynamodb.scan(
            TableName=table,
            FilterExpression='tenant_id = :tenant_id',
            ExpressionAttributeValues={':tenant_id': {'S': tenant_id}}
        )

        schedules: dict = {}
        for item in response['Items']:
            code: str = item['code']['S']
            value: str = item['horario']['S'].replace("'", "\"")

            data: list = ast.literal_eval(value) 

            schedule: dict = { item['dia']: item['horas'] for item in data }
            days: list = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
            for day in days:
                schedule.setdefault(day, [])
            schedules[code] = schedule

        for code in schedules.keys():
            member: dict = get_member(code)
            schedules[code]['nombre'] = member['nombre']
            schedules[code]['correo'] = member['correo']

        return schedules
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)