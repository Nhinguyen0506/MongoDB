pass_fail_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["applicationDate"],
        
        "properties": {
            
            "applicationDate": {
                "bsonType": "date"
            }
            #Inherits other properties from Enrollment
        }
    }
}

