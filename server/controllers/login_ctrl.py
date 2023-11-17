from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from database.db import dynamodb
from typing import Optional

table = 't_usuarios'

def login(id: str, password: str) -> Optional[dict]:
    
    try:
        partial_id = id

        scan_filter_expression = 'begins_with(id, :partial_id)'
        expression_attribute_values = {':partial_id': {'S': partial_id}}

        response = dynamodb.scan(
            TableName=table,
            FilterExpression=scan_filter_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        if(response['Count'] != 0):
            if(password == str(response['Items'][0]['password']['S'])): 
                data: dict = {
                    'tenant_id': str(response['Items'][0]['tenant_id']['S']),
                    'rol': str(response['Items'][0]['rol']['S'])
                }
                return data
            else:
                return JSONResponse(content={"error": "Contraseña incorrecta"}, status_code=401)
        else:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

        
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)
