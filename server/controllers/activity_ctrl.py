from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from database.db import dynamodb
from typing import Optional

table = 't_actividades'

def get_activities(tenant_id: str = 'UTEC') -> Optional[dict]: ##
    activities: list = []
    try:
        response: dict = dynamodb.scan(
            TableName=table,
            FilterExpression='tenant_id = :tenant_id',
            ExpressionAttributeValues={':tenant_id': {'S': tenant_id}}
        )
        for item in response['Items']:
            it = {
                "activity_id": item['activity_id']['S'],
                "calificacion": item['calificacion']['N'],
                "cant_person": item['cant_person']['N'],
                "description": item['description']['S'],
                "duracion": item['duracion']['N'],
                "min_person": item['min_person']['N'],
                "name": item['name']['S'],
                "tipo": item['tipo']['S']
            }
            activities.append(it)
        return {'content': activities}
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)


def get_activity(activity_id: str, tenant_id = 'UTEC') -> Optional[dict]: ##
    try:
        response: dict = dynamodb.get_item(
            TableName=table,
            Key={
                'tenant_id': {'S': tenant_id}, 
                'activity_id': {'S': activity_id}
            },
        )
        
        item: dict = response.get('Item', {})
        it = {
            "name": item['name']['S'],
            "description": item['description']['S'],
            "cant_person": item['cant_person']['N'],
            "min_person": item['min_person']['N'],
            "duracion": item['duracion']['N'],
            "tipo": item['tipo']['S'],
            "calificacion": item['calificacion']['N']
        }
        return {item['activity_id']['S'] : it}
        
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)
