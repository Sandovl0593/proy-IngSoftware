import csv
import boto3
from os import getenv

aws_access_key_id="ASIA6A6UW7LWVA4GUQ4E"
aws_secret_access_key="dxQ1Prv//cg/nfW1vlmIx/8y26uDHK7hHmVPJyIN"
aws_session_token="FwoGZXIvYXdzEPH//////////wEaDBxIV5zK9PUnKpdlqCLNAabJjGvOCsfJ4onK3FBtEvoP245WsA+QHmnSKBnc11GPGf5w3xwjNdWi7nw7ENOTSyOAgEndgR7DGFH5DzL7wbPbZakrfoPOaXuRxUEkxQJ5pFSebtkuXOMIWt3hO62BbaheA/LJVGrw3GWDInPsRwohf0lvuJEI9+IduJXETwE0XyF385Vju12em0jyLRODMqlAJhkiKhBy2MBEx60Od2ULoqZ6vdHUriI76tgOoY1ogTR6Oy1Cbzv10wM6KqMZyG9chKafHiWNxzsARpwogpr6qgYyLXsFtrSd3qtBEsfXHlhOUwLhxf1ligiwnynRf6No4oPPDjGa9OhvVoAl27uZ7Q=="
aws_region_name="us-east-1"

def get_ids_activity(code_member):
    # Crea un cliente de PersonalizationEvents
    personalize_runtime = boto3.client('personalize-runtime',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=aws_region_name)
    

    # Define los parámetros para la llamada a la API
    params = {
        'campaignArn': 'arn:aws:personalize:us-east-1:964129389293:campaign/campaign',
        'userId': f'{code_member}',
        'numResults': 20,
    }

    # Realiza la llamada a la API
    response = personalize_runtime.get_recommendations(**params)
    # Imprime la respuesta
    ids_act = [] 
    for i in response['itemList']:
        ids_act.append(i['itemId'])
    print(response['itemList'])
    print(ids_act)
    return ids_act

get_ids_activity('202320831')