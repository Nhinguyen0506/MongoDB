
enrollment_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["enrollment_category_data"],
        "properties": {
            '_id': {},
            "last_name": {
                "bsonType": "string",
                "maxLength": 32
            },
            "first_name": {
                "bsonType": "string",
                "maxLength": 32
            },
            "department_abbreviation": {
                "bsonType": "string",
                "maxLength": 6
            },
            'course_number': {
                'bsonType': "int",
                'minimum': 100,
                'maximum': 699,
                "description": "A 3-digit number designating a specific course within a department."
            },
            "section_number": {
                "bsonType": "int",
                "minimum": 0,
                "maximum": 20
            },
            "enrollment_category_data": {
                'oneOf': [
                    {
                        'bsonType': 'object',
                        'required': ['type', 'application_date'],
                        'additionalProperties': False,
                        'properties': {
                            'type': {
                                'bsonType': 'string'
                            },
                            'application_date': {
                                'bsonType': 'date',
                            }
                        }
                    },
                    {
                        'bsonType': 'object',
                        'required': ['type', 'min_satisfactory'],
                        'additionalProperties': False,
                        'properties': {
                            'type': {
                                'bsonType': 'string'
                            },
                            'min_satisfactory': {
                                "bsonType": "string",
                                "enum": ["A", "B", "C"]
                            }
                        }
                    }
                ]
            }

            # 'enrollment_category_data': {
            # 'oneOf': [
            #     {
            #         "bsonType": "object",
            #         'required': ['applicationDate'],
            #         'additionalProperties': False,
            #         "properties": {
            #             'applicationDate': {
            #                 'bsonType': 'date',
            #                 'maximum': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            #             }
            #         }
            #     },
            #     # The next element of the oneOf array is, itself a oneOf, which would correspond to
            #     # a categorization of a category.
            #     {
            #         "bsonType": "object",
            #         'required': ['minSatisfactory'],
            #         'additionalProperties': False,
            #         "properties": {
            #             'minSatisfactory': {
            #                 "bsonType": "string",
            #                 "enum": ["A", "B", "C"]
            #             },
            #             # Here is where we "plug in" the student_category_data variable to finish off
            #             # the enclosing person_validator variable so that it's more readable.
            #
            #         }
            #     }
            # ]
            # }
        }
    }
}
