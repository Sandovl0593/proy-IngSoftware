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
            configuracion['list'] = item['list']['N']
            configuracion['face_graphic'] = item['face_graphic']['N']

        return {'content': configuracion}
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)


