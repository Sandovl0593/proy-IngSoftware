import boto3
import csv

# Configurar el cliente de DynamoDB con tus credenciales
aws_access_key_id="ASIA6A6UW7LW3QMZZR2W"
aws_secret_access_key="QtcNJtP0l5u8YfeAWiYgj6lBV3yQ5mkgPZC6v3Ti"
aws_session_token="FwoGZXIvYXdzEOj//////////wEaDCO66epxIZLfz7ys2yLNAWEDM0KQVRlhWj4A/+EgdZpOpmJLO0S+QuC+Dz1mpzD6IdQlR7NnDWF8pUMP9gbACFTn4g1mWfBiTyqa+BXaRNEC6az7vb57axD4Jh15zVgky1yEYrR6mZCLVoR4PnWuqIm2ABitiHe9KWtxHM+9HD4o/IjVxLhfWKKyii7MF6iqtUqZJ9E0df9Kfp7EMEc1T/PD6YGv1BbWegiuAoJnyCtOKB4ImEDUbHg3bFmYH9/6CRcn6FiBdF2WK9ZAdvzWd4DVLhWfm/JQE3Z5ErUo16P4qgYyLVOSLc/z+dQqCNDsreWLxh/4to3AW5bYk9FibOfu1zMQpqT6FlKePZKdUJrPfw=="
region_name = 'us-east-1'


aws_access_key_id=ASIA6A6UW7LW3QMZZR2W
aws_secret_access_key=QtcNJtP0l5u8YfeAWiYgj6lBV3yQ5mkgPZC6v3Ti
aws_session_token=FwoGZXIvYXdzEOj//////////wEaDCO66epxIZLfz7ys2yLNAWEDM0KQVRlhWj4A/+EgdZpOpmJLO0S+QuC+Dz1mpzD6IdQlR7NnDWF8pUMP9gbACFTn4g1mWfBiTyqa+BXaRNEC6az7vb57axD4Jh15zVgky1yEYrR6mZCLVoR4PnWuqIm2ABitiHe9KWtxHM+9HD4o/IjVxLhfWKKyii7MF6iqtUqZJ9E0df9Kfp7EMEc1T/PD6YGv1BbWegiuAoJnyCtOKB4ImEDUbHg3bFmYH9/6CRcn6FiBdF2WK9ZAdvzWd4DVLhWfm/JQE3Z5ErUo16P4qgYyLVOSLc/z+dQqCNDsreWLxh/4to3AW5bYk9FibOfu1zMQpqT6FlKePZKdUJrPfw==
region_name=us-east-1

dynamodb = boto3.client('dynamodb', 
                          aws_access_key_id=aws_access_key_id, 
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token,
                          region_name=region_name
                          )

table = 't_actividades'

with open('updated_activities.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        item = {
            'tenant_id': {'S': row['tenant_id']},
            'activity_id': {'S': row['activity_id']},
            'name': {'S': row['name']},
            'emotion': {'S' : row['emotion']},
            'description': {'S': row['description']},
            'cant_person': {'N': row['cant_person']},
            'min_person': {'N': row['min_person']},
            'duracion': {'N': row['duracion']},
            'tipo': {'S': row['tipo']},
            'calificacion': {'N': row['calificacion']}
        }
        print(item)
        dynamodb.put_item(
            TableName=table,
            Item=item
        )
print(csvreader)

