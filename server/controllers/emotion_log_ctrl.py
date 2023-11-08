from server.database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from collections import defaultdict
from typing import Optional

table = 't_registro_emociones'


def get_emotion_logs_member(member_code: str, from_date: str, tenant_id: str = 'UTEC') -> Optional[dict]:
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


def get_emotion_logs(from_date: str, tenant_id: str = 'UTEC') -> Optional[dict]:
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


# Auxiliary Functions

def get_emotion_member_codes(items: dict) -> dict:
    emotions: defaultdict = defaultdict(list)
    for item in items:
        emotion: str = item['emocion']['S']
        code: str = item['code']['S']
        emotions[emotion].append(code)

    return dict(emotions)
