from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from server.database.db import dynamodb
from typing import Optional

table = 't_areas'


def get_areas(tenant_id: str = 'UTEC') -> Optional[dict]:
    areas: list = []

    try:
        response: dict = dynamodb.scan(
            TableName=table
        )
        for item in response['Items']:
            if item['tenant_id']['S'] == tenant_id:
                name: str = item['nombre']['S']
                areas.append(name)
        print(areas)
        return {'content': areas}
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)
