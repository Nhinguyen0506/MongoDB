student_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["last_name", "first_name", "e_mail"],
        "properties": {
            "last_name": {
                "bsonType": "string",
                "maxLength": 32
            },
            "first_name": {
                "bsonType": "string",
                "maxLength": 32
            },
            "e_mail": {
                "bsonType": "string",
                "maxLength": 127
            },
            'student_major': {
                'bsonType': 'array',
                'items': {
                    'bsonType': 'object',
                    'required': ['major_id', 'major_name', 'declaration_date'],
                    'properties': {
                        'major_name': {
                            'bsonType': 'string',
                        },
                        'declaration_date': {
                            'bsonType': 'date',
                        }
                    }
                }
            }
        }
    }
}
