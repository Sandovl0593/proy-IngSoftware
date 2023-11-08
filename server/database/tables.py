from typing import List, Dict, Any

tables: List[Dict[str, Any]] = [
    {
        "TableName": "Member",
        "KeySchema": [
            {
                'AttributeName': 'code',
                'KeyType': 'HASH'
            }
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': 'code',
                'AttributeType': 'S'
            }
        ]
    },
    {
        "TableName": "EmotionLog",
        "KeySchema": [
            {
                "AttributeName": "member_code",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "timestamp",
                "KeyType": "RANGE"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "member_code",
                "AttributeType": "S"
            },
            {
                "AttributeName": "timestamp",
                "AttributeType": "S"
            }
        ]
    }, 
    {
        "TableName": "Area",
        "KeySchema": [
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            }
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            }
        ]
    },
    {
        "TableName": "PsychologistSchedule",
        "KeySchema": [
            {
                'AttributeName': 'member_code',
                'KeyType': 'HASH'
            }
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': 'member_code',
                'AttributeType': 'S'
            }
        ]
    },
    {
        "TableName": "Emotion",
        "KeySchema": [
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            }
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            }
        ]
    },
    {
        "TableName": "Rol",
        "KeySchema": [
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            }
        ],
        "AttributeDefinitions": [
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            }
        ]
    }
]
