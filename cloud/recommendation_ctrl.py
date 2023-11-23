from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from controllers.emotion_ctrl import get_emotion_names
from controllers.activity_ctrl import get_activity
from database.db import dynamodb
from typing import Optional
from collections import Counter
import random
import boto3
from os import getenv

table = 't_recomendaciones_emocion'


def get_recommedation(tenant_id: str = 'UTEC') -> Optional[dict]: ##
    recomm = {}
    try:
        response: dict = dynamodb.scan(
            TableName=table,
            FilterExpression='tenant_id = :tenant_id',
            ExpressionAttributeValues={':tenant_id': {'S': tenant_id}}
        )
        for item in response['Items']:
            emocion: str = item['emocion']['S']
            activities: str = item['activity']['S'].split('|')
            act = activities.copy()
            # Obtener una distribución aleatoria de la copia
            random.shuffle(act)
            #print(recomm)
            recomm[emocion] = {
                'actividad': [get_activity(activity) for activity in act]
            }
            #print(recomm)

        return recomm
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)

