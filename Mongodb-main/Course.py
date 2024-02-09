course_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["course_number", "course_name", "description", "units"],
        "properties": {
            'course_number': {
                'bsonType': "int",
                'minimum': 100,
                'maximum': 699,
                "description": "A 3-digit number designating a specific course within a department."
            },
            "course_name": {
                "bsonType": "string",
                "maxLength": 60
            },
            "description": {
                "bsonType": "string",
                "maxLength": 80
            },
            "units": {
                "bsonType": "int",
                "minimum": 1,
                "maximum": 5
            }
        }
    }
}
