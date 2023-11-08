from controllers.emotion_log_ctrl import get_emotion_logs
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from database.db import dynamodb
from collections import Counter
from datetime import datetime
from typing import Optional

table = 't_emociones'

def get_emotion_scores(tenant_id: str ='UTEC') -> Optional[dict]: ##
    try:
        response: dict = dynamodb.scan(
            TableName=table
        )

        emotions: dict = {}
        for item in response['Items']:
            if(item['tenant_id']['S'] == tenant_id):
                name: str = item['nombre']['S']
                score: int = int(item['valor']['N'])
                emotions[name] = score
        
        return emotions   
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)


def get_emotion_names() -> Optional[dict]: ##
    try:
        data_emotions = get_emotion_scores()
        emotions = list(data_emotions.keys())
        return {'content': emotions}

    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)


def get_emotion_predominant() -> Optional[dict]:  ##
    from_date: str = datetime(2023, 8, 28).strftime('%Y-%m-%d')#debería ser today -2 
    # end_date: str = datetime.now().strftime('%Y-%m-%d')

    try:
        items: dict = get_emotion_logs(from_date)
        emotions: list = [item['emocion']['S'] for item in items]
        emotion_counter: Counter = Counter(emotions)
        emotion_total_values: len = len(emotions) #
        emotion_predominant: str = emotion_counter.most_common(1)[0][0]
        emotion_predominant_percentage: float = round(int(emotion_counter.most_common(1)[0][1]) * 100/emotion_total_values,2)
        return {'content': (emotion_predominant,emotion_predominant_percentage)}
    
    except ClientError as e:
        return JSONResponse(content=e.response['Error'], status_code=500)