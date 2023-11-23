from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from controllers.emotion_ctrl import get_emotion_names

from typing import Optional
from collections import Counter
import boto3
from os import getenv

aws_access_key_id="ASIA6A6UW7LW3GEPKMIA"
aws_secret_access_key="81zZ7ww4kCfpPZ6bX8WUHOCmfDHcoP7LRpNsPfzN"
aws_session_token="FwoGZXIvYXdzEPb//////////wEaDHGuv6W3MFq2ijsKDSLNAY8z6qMyb5T1wRsz6Ro1a0aDu5T+sYh+lbug3cS+efcs67gZ67jKwPS0HgT8O30AgibUe/GORlYi/bx6MHzjJqM8/URK09eg7qprxd3+uhQG3p8si9kt0hlD/p2JIXdJkqoB0w99dUvnmv3ucFZAj2qJZjNtUELy8gnVxLyMG0npzrBv5pzClQOFn9Lwwbe2kKHTrgTE0LwYKrbLlcmMq88mwnueAvw+kRlG4TPf9LlI+XCNcvcJQXxksZsylLV6s5Cm7vCnGa06IEpwuEQopK37qgYyLYLsU0/XzNWGfjqV/Bi1yiHM1cy7ic2tPVBd5mg6TDB5VwoiJy8reTsjo62XFQ=="
aws_region_name="us-east-1"


# Configura el cliente de DynamoDB
dynamodb = boto3.client('dynamodb',
         aws_access_key_id=aws_access_key_id,
         aws_secret_access_key=aws_secret_access_key,
         aws_session_token=aws_session_token,
         region_name=aws_region_name
        )


table = 't_recommendation'
table_em_mem = 't_emociones_miembros'

recommedations = {
    'felicidad': [],
    'motivacion': [],
    'satisfaccion': [],
    'alivio': [],
    'aburrimiento': [],
    'preocupacion': [],
    'estres': [],
    'frustracion': [],
    'ansiedad': [],
    'enojo': [],
    'tristeza': []
}

def get_recommedation(tenant_id: str = 'UTEC') -> Optional[dict]: ##
    members = []
    members_dict = {}
    response: dict = dynamodb.scan(
        TableName=table_em_mem,
        FilterExpression='tenant_id = :tenant_id',
        ExpressionAttributeValues={':tenant_id': {'S': tenant_id}}
    )
    for item in response['Items']:
        code: str = item['code']['S']
        emotion: str = item['main_emotion']['S']
        members.append([code, emotion])
    #print(members)

    i = 0
    for member in members:
        ids_activity = get_ids_activity(member[0])
        print("------------------------------>", i, member[0])
        i+=1
        #print(members_dict)
        members_dict[member[0]] = ids_activity
        #print(members_dict)
        # if i == 5: break #

    print(members_dict)
    print(members)
    for member in members:
        if (member[1] == 'felicidad'):
            recommedations['felicidad'] += members_dict[member[0]]
        elif (member[1] == 'motivacion'):
            recommedations['motivacion'] += members_dict[member[0]]
        elif (member[1] == 'satisfaccion'):
            recommedations['satisfaccion'] += members_dict[member[0]]
        elif (member[1] == 'tristeza'):
            recommedations['tristeza'] += members_dict[member[0]]
        elif (member[1] == 'aburrimiento'):
            recommedations['aburrimiento'] += members_dict[member[0]]
        elif (member[1] == 'preocupacion'):
            recommedations['preocupacion'] += members_dict[member[0]]
        elif (member[1] == 'estres'):
            recommedations['estres'] += members_dict[member[0]]
        elif (member[1] == 'frustracion'):
            recommedations['frustracion'] += members_dict[member[0]]
        elif (member[1] == 'ansiedad'):
            recommedations['ansiedad'] += members_dict[member[0]]
        elif (member[1] == 'enojo'):
            recommedations['enojo'] += members_dict[member[0]]
        else:
            recommedations['alivio'] += members_dict[member[0]]

    recomm = {}
    for emotion, ids in recommedations.items():
        contador_nombres = Counter(ids)
        # Obtener los 20 más comunes y extraer solo las claves
        ids_ = [id_ for id_, _ in contador_nombres.most_common(25)]
        recomm[emotion] = ids_
    #print(recomm)
    return recomm


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
    #print(response['itemList'])
    #print(ids_act)
    return ids_act


def main():
    res = get_recommedation()
    table_name = 't_recomendaciones_emocion'
    #res =

    # Lee el archivo CSV y carga los datos a DynamoDB
    for em in res.keys():
        # Convierte los tipos según sea necesario (puedes ajustar esto según tu esquema)
        item = {
            'tenant_id': {'S': 'UTEC'},
            'emocion': {'S': str(em)},
            'activity': {'S': '|'.join(res[em])}
        }
        print(item)

    # Añade el item a la tabla DynamoDB
        dynamodb.put_item(
            TableName=table_name,
            Item=item
        )

    print(f'Datos importados a la tabla DynamoDB: {table_name}')


main()
