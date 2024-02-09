major_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["department_abbreviation", "name", "description"],
        "properties": {
            "department_abbreviation": {
                "bsonType": "string",
                "maxLength": 6
            },
            "name": {
                "bsonType": "string",
            },
            "student_ids": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                }
            },
            "description": {
                "bsonType": "string",
                "maxLength": 80
            }
        }
    }
}
