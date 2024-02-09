import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu

# MongoDB connection string
connection_string = "mongodb+srv://nguyenkevin828:Password@cecs-323-spring-2023.qhst2lw.mongodb.net/?retryWrites=true&w=majority"

# Use the connection string to connect to MongoDB
client = MongoClient(connection_string)

# Database name
db = client["CECS-323-Spring-2023"]

# Define the schema for the Department collection
department_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "abbreviation", "chair_name", "building", "description"],
        "properties": {
            "name": {
                "bsonType": "string",
                "minLength": 10,
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
                "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
            },
            "office": {
                "bsonType": "int",
                "minimum": 1,
                "maximum": 1000
            },
            "description": {
                "bsonType": "string",
                "minLength": 10,
                "maxLength": 80
            }
        }
    }
}

# Create the "departments" collection with the schema
db.create_collection("departments", validator=department_schema)

# Add uniqueness constraints to the collection
db.departments.create_index([("name", pymongo.ASCENDING)], unique=True)
db.departments.create_index([("abbreviation", pymongo.ASCENDING)], unique=True)
db.departments.create_index([("chair_name", pymongo.ASCENDING)], unique=True)
db.departments.create_index([("building", pymongo.ASCENDING), ("office", pymongo.ASCENDING)], unique=True)



def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_student(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["students"]
    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''
    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = collection.count_documents({"e_mail": email})
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address.  Try again.")
    # Build a new students document preparatory to storing it
    student = {
        "last_name": lastName,
        "first_name": firstName,
        "e_mail": email
    }
    results = collection.insert_one(student)


def select_student(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from 
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student


def delete_student(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    student = select_student(db)
    # Create a "pointer" to the students collection within the db database.
    students = db["students"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = students.delete_one({"_id": student["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} students.")


def list_student(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for student in students:
        pprint(student)


# Function to add a new department
def add_department(db):
    print("Add a New Department")

    # Collect department data based on the schema
    department_data = {}

    for field, constraints in department_schema['$jsonSchema']['properties'].items():
        while True:
            try:
                value = input(f"{field.replace('_', ' ').capitalize()}: ")
                if constraints['bsonType'] == "string":
                    min_length = constraints.get("minLength", 0)
                    max_length = constraints.get("maxLength", float('inf'))
                    if min_length <= len(value) <= max_length:
                        department_data[field] = value
                        break
                    else:
                        print(f"{field.capitalize()} must be between {min_length} and {max_length} characters.")
                elif constraints['bsonType'] == "int":
                    minimum = constraints.get("minimum", float('-inf'))
                    maximum = constraints.get("maximum", float('inf'))
                    value = int(value)
                    if minimum <= value <= maximum:
                        department_data[field] = value
                        break
                    else:
                        print(f"{field.capitalize()} must be between {minimum} and {maximum}.")
                else:
                    print(f"{field.capitalize()} does not meet the specified constraints.")
            except ValueError:
                print(f"Error: Invalid input for {field}. Please enter a valid value.")
            except KeyError:
                print(f"Error: Missing data for {field}. Please provide the required information.")

    try:
        # Insert the new department into the MongoDB collection
        db.departments.insert_one(department_data)
        print("Department added successfully.")
    except pymongo.errors.DuplicateKeyError as e:
        print(f"Error: Department with the same data already exists. Please enter unique department data.")
        add_department(db)  # Re-prompt the user for department data
    except Exception as e:
        print(f"Error: {e}. Please re-enter department data.")
        add_department(db)  # Re-prompt the user for department data





# Function to delete a department
def delete_department(db):
    print("Delete a Department")
    list_department(db)  # List available departments

    name = input("Enter the name of the department to delete: ")

    # Check if the department exists
    department = db.departments.find_one({"name": name})
    if department:
        # Delete the department
        db.departments.delete_one({"name": name})
        print("Department deleted successfully.")
    else:
        print(f"Department '{name}' not found.")


# Function to list all departments
def list_department(db):
    print("List of Departments")
    departments = db.departments.find().sort("name")

    for department in departments:
        print(department)


def boilerplate(db):
    preload_departments = [
        {
            "name": "Computer Science",
            "abbreviation": "CS",
            "chair_name": "John Smith",
            "building": "ECS",
            "description": "Computer Science ",
        },
        {
            "name": "Biology Department",
            "abbreviation": "BIO",
            "chair_name": "Sarah Johnson",
            "building": "CDC",
            "description": "Biology",  #
        },
        {
            "name": "Physics Department ",
            "abbreviation": "PHY",
            "chair_name": "Robert Davis",
            "building": "EN2",
            "description": "Physics Department",
        },
    ]

    for department_data in preload_departments:
        if all(field in department_data for field in department_schema['$jsonSchema']['required']):
            # Check if the department data includes all required fields
            db.departments.insert_one(department_data)
        else:
            print("Invalid department data. Make sure it includes all required fields.")



if __name__ == '__main__':
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
