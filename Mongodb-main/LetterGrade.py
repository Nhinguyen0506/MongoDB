letter_grade_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["minSatisfactory"],
        
        "properties": {
            
            "minSatisfactory": {
                "bsonType": "string",
                "enum": ["A", "B", "C"]
            }
            #Inherits other properties from Enrollment
        }
    }
}

