department_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "abbreviation", "chair_name", "building", "office", "description"],
        "properties": {
            "name": {
                "bsonType": "string",
                "minLength": 5,
                "maxLength": 50
            },
            "abbreviation": {
                "bsonType": "string",
                "maxLength": 6
            },
            "chair_name": {
                "bsonType": "string",
                "maxLength": 80
            },
            "building": {
                "bsonType": "string",
                "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4'
                    , 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
            },
            "office": {
                "bsonType": "int",
                "minimum": 1,
                "maximum": 1000
            },
            "description": {
                "bsonType": "string",
                "maxLength": 80
            }
        }
    }
}


def select_department(db):
    collection = db["departments"]
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Department's abbreviation-->")
        abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department found by that abbreviation. Try again.")
    found_department = collection.find_one({"abbreviation": abbreviation})
    return found_department
