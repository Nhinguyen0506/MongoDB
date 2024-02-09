section_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["section_number", "semester", "section_year", "building", "room",
                     "schedule", "start_hour", "start_minute", "instructor"],

        "properties": {
            "section_number": {
                "bsonType": "int",
                "minimum": 0,
                "maximum": 20
            },
            "semester": {
                "bsonType": "string",
                "enum": ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter']
            },
            "section_year": {
                "bsonType": "int",
                "minimum": 2000,
                "maximum": 3000
            },
            "building": {
                "bsonType": "string",
                "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4'
                    , 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
            },
            "room": {
                "bsonType": "int",
                "minimum": 1,
                "maximum": 999
            },
            "schedule": {
                "bsonType": "string",
                "enum": ['MW', 'TuTh', 'MWF', 'F', 'S']
            },
            'start_hour': {
                'bsonType': "int",
                "description": "The hour when the section starts.",
                "minimum": 8,
                "maximum": 19
            },
            'start_minute': {
                'bsonType': "int",
                'description': "The minutes into the start_hour when the section starts.",
                'enum': [0, 30],
            },
            "instructor": {
                "bsonType": "string",
                "maxLength": 80
            }
        }
    }
}
