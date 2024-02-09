complete_incomplete_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["student_id", "department_abbreviation", "course_number", "section_number", "semester",
                     "section_year", "completion_status"],
        
        "properties": {
            
            "student_id": {
                "bsonType": "objectId",
                "description": "Reference to the student document"
            },
            "department_abbreviation": {
                "bsonType": "string",
                "description": "Abbreviation of the department offering the section"
            },
            "course_number": {
                "bsonType": "int",
                "description": "Number of the course"
            },
            "section_number": {
                "bsonType": "int",
                "description": "Number of the section within the course"
            },
            "semester": {
                "bsonType": "string",
                "description": "Semester in which the section is offered"
            },
            "section_year": {
                "bsonType": "int",
                "description": "Year in which the section is offered"
            },
            "completion_status": {
                "bsonType": "string",
                "enum": ["Completed", "Incomplete"],
                "description": "Status indicating whether the student has completed the course"
            }
        }
    }
}
