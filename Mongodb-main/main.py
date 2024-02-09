import pymongo
from pymongo import MongoClient
import datetime
from pprint import pprint

import Major
import Student
import menu_definitions
import Department
import Course
import Section
import Enrollment
# MongoDB connection string
connection_string = "mongodb+srv://antran01:chuot299@project1.ryybymr.mongodb.net/?retryWrites=true&w=majority"
# Use the connection string to connect to MongoDB
client = MongoClient(connection_string)

# Database name
db = client["university"]

# SCHEMAS FIELD
# Department.department_schema
# Course.course_schema
# Section.section_schema

# Create the collection with the schema
# db.create_collection("departments", validator=Department.department_schema)
# db.create_collection("courses", validator=Course.course_schema)
# db.create_collection("sections", validator=Section.section_schema)
# db.create_collection("majors", validator=Major.major_schema)
# db.create_collection("students", validator=Student.student_schema)
# db.create_collection("enrollments", validator=Enrollment.enrollment_schema)

try:
    db.create_collection("departments", validator=Department.department_schema)
except Exception as e:
    pass
try:
    db.create_collection("courses", validator=Course.course_schema)
except Exception as e:
    pass
try:
    db.create_collection("sections", validator=Section.section_schema)
except Exception as e:
    pass
try:
    db.create_collection("majors", validator=Major.major_schema)
except Exception as e:
    pass
try:
    db.create_collection("students", validator=Student.student_schema)
except Exception as e:
    pass
try:
    db.create_collection("enrollments", validator=Enrollment.enrollment_schema)
except Exception as e:
    pass
# Define the collections
department_collection = db['departments']
course_collection = db['courses']
section_collection = db['sections']
enrollment_collection = db['enrollments']
complete_incomplete_collection = db['complete_incomplete']

# Add uniqueness constraints to the department collection
db.departments.create_index([("name", pymongo.ASCENDING)], unique=True)
db.departments.create_index([("abbreviation", pymongo.ASCENDING)], unique=True)
db.departments.create_index([("chair_name", pymongo.ASCENDING)], unique=True)
db.departments.create_index([("building", pymongo.ASCENDING), ("office", pymongo.ASCENDING)], unique=True)
db.departments.create_index([("description", pymongo.ASCENDING)], unique=True)

# Add uniqueness constraints to the course collection
db.courses.create_index([("course_name", pymongo.ASCENDING), ("department_abbreviation", pymongo.ASCENDING)],
                        unique=True)
db.courses.create_index([("course_number", pymongo.ASCENDING), ("department_abbreviation", pymongo.ASCENDING)],
                        unique=True)
db.courses.create_index([("description", pymongo.ASCENDING)], unique=True)

# Add uniqueness constraints to the section collection
db.sections.create_index([("section_year", pymongo.ASCENDING),
                          ("department_abbreviation", pymongo.ASCENDING),
                          ("course_number", pymongo.ASCENDING),
                          ("section_number", pymongo.ASCENDING),
                          ("semester", pymongo.ASCENDING)], unique=True)
db.sections.create_index([("section_year", pymongo.ASCENDING),
                          ("semester", pymongo.ASCENDING),
                          ("schedule", pymongo.ASCENDING),
                          ("start_time", pymongo.ASCENDING),
                          ("building", pymongo.ASCENDING),
                          ("room", pymongo.ASCENDING)], unique=True)
db.sections.create_index([("section_year", pymongo.ASCENDING),
                          ("semester", pymongo.ASCENDING),
                          ("schedule", pymongo.ASCENDING),
                          ("start_time", pymongo.ASCENDING),
                          ("instructor", pymongo.ASCENDING)], unique=True)
db.enrollments.create_index([("section_year", pymongo.ASCENDING),
                             ("department_abbreviation", pymongo.ASCENDING),
                             ("course_number", pymongo.ASCENDING),
                             ("semester", pymongo.ASCENDING), ("student_id", pymongo.ASCENDING)], unique=True)
db.enrollments.create_index([("student_id", pymongo.ASCENDING),
                             ("section_id", pymongo.ASCENDING), ], unique=True)
# Add uniqueness constraints to the student collection
db.students.create_index([("last_name", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING)],
                         unique=True, name="students_full_name")
db.students.create_index([("e_mail", pymongo.ASCENDING)], unique=True, name="students_email")

# Add uniqueness constraints to the major collection
db.majors.create_index([("name", pymongo.ASCENDING)], unique=True)


# Join course and section using course_number:


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != menu_definitions.add_menu.last_action():
        add_action = menu_definitions.add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != menu_definitions.delete_menu.last_action():
        delete_action = menu_definitions.delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != menu_definitions.list_menu.last_action():
        list_action = menu_definitions.list_menu.menu_prompt()
        exec(list_action)


# DEPARTMENT PARTS
def add_department(db):
    print("Add a New Department")

    # Collect department data based on the schema
    department_data = {}

    for field, constraints in Department.department_schema['$jsonSchema']['properties'].items():
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
    if db.departments.count_documents({}) == 0:
        print("No department to delete")
        return
    abbreviation = input("Enter the abbreviation of the department to delete: ")
    # Check if the department still have course
    courses_count = db.courses.count_documents({"department_abbreviation": abbreviation})
    if courses_count > 0:
        print(
            f"Cannot delete the department as it still have {courses_count} courses. Please delete all courses and try again.")
        return
        # Check if the department exists
    department = db.departments.find_one({"abbreviation": abbreviation})
    if department:
        # Delete the department
        db.departments.delete_one({"abbreviation": abbreviation})
        print("Department deleted successfully.")
    else:
        print(f"Department {abbreviation} not found.")
        delete_department(db)


# Function to list all departments
def list_department(db):
    print("List of Departments")
    departments = db.departments.find().sort("name")

    for department in departments:
        print(department)


# COURSES PARTS
def add_course(db):
    print("Add a New Course")
    department_abbreviation = ''
    department = ''
    # Find department to add a course
    found = False
    while not found:
        department_abbreviation = input("Enter department abbreviation for the course: ")
        department = department_collection.find_one({'abbreviation': department_abbreviation})
        if department is None:
            print("There is no department with that abbreviation. Please ensure that the abbreviation exists. "
                  "Please enter it again.")
            found = False
        else:
            found = True
    # Collect course data based on the schema
    course_data = {}
    course_data['department_abbreviation'] = department_abbreviation
    course_data['department_name'] = department.get('name', '')
    for field, constraints in Course.course_schema['$jsonSchema']['properties'].items():
        while True:
            try:
                value = input(f"{field.replace('_', ' ').capitalize()}: ")
                if constraints['bsonType'] == "string":
                    min_length = constraints.get("minLength", 0)
                    max_length = constraints.get("maxLength", float('inf'))
                    if min_length <= len(value) <= max_length:
                        course_data[field] = value
                        break
                    else:
                        print(f"{field.capitalize()} must be between {min_length} and {max_length} characters.")
                elif constraints['bsonType'] == "int":
                    minimum = constraints.get("minimum", float('-inf'))
                    maximum = constraints.get("maximum", float('inf'))
                    value = int(value)
                    if minimum <= value <= maximum:
                        course_data[field] = value
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

        # Insert the new course into the MongoDB collection
        db.courses.insert_one(course_data)
        db.departments.update_one(
            {"abbreviation": department_abbreviation},
            {"$addToSet": {"courses": {"course_number": course_data['course_number'],
                                       "course_name": course_data['course_name']}}},
        )
        print("Course added successfully.")
    except pymongo.errors.DuplicateKeyError as e:
        print(f"Error: Course with the same data already exists. Please enter unique course data.")
        add_course(db)  # Re-prompt the user for course data
    except Exception as e:
        print(f"Error: {e}. Please re-enter department data.")
        add_course(db)  # Re-prompt the user for course data


# Function to delete a course
def delete_course(db):
    print("Delete a Course")
    list_course(db)  # List available courses
    if db.courses.count_documents({}) == 0:
        print("No course to delete")
        return
    found = False
    while not found:
        try:
            abbreviation = input("Enter the abbreviation of the course to delete: ").strip().upper()
            course_number = int(input("Enter the course number of the course to delete: "))
            sections_count = db.sections.count_documents({"department_abbreviation": abbreviation,
                                                          "course_number": course_number})

            if sections_count > 0:
                print(f"Cannot delete the department as it still have {sections_count} courses. "
                      f"Please delete all courses and try again.")
                return
            # Check if the course exists
            course = db.courses.find_one({"course_number": course_number, "department_abbreviation": abbreviation})

            if course:
                # Delete the course
                db.courses.delete_one({"course_number": course_number, "department_abbreviation": abbreviation})
                print("Course deleted successfully.")
                found = True
            else:
                print(f"Course {abbreviation} {course_number} not found.")
        except ValueError:
            print(f"Error: Invalid input. Please enter a valid value.")


# Function to list all courses
def list_course(db):
    print("List of Courses")
    courses = db.courses.find().sort("course_number")

    for course in courses:
        print(course)


def add_section(db):
    print("Add a New Section")
    department_abbreviation = ''
    course_number = ''
    course = ''
    department = ''
    # Find department and course number to add a section
    found = False
    while not found:
        try:
            department_abbreviation = input("Enter department abbreviation for the section: ").strip().upper()
            department = department_collection.find_one({'abbreviation': department_abbreviation})
            course_number = int(input("Enter course number for the section: "))
            course = course_collection.find_one({'course_number': course_number},
                                                {'abbreviation': department_abbreviation})
            if department is None:
                print("There is no department with that abbreviation. Please ensure that the abbreviation exists. "
                      "Please enter it again.")
            elif course is None:
                print("There is no course with that number. Please ensure that the course number exists. "
                      "Please enter it again.")
            else:
                found = True
        except ValueError:
            print(f"Error: Invalid input. Please enter a valid value.")
    # Collect section data based on the schema
    section_data = {}
    section_data['department_abbreviation'] = department_abbreviation
    section_data['course_number'] = course_number
    section_data['course_name'] = course.get('course_name', '')
    for field, constraints in Section.section_schema['$jsonSchema']['properties'].items():
        while True:
            try:
                value = input(f"{field.replace('_', ' ').capitalize()}: ")
                if constraints['bsonType'] == "string":
                    min_length = constraints.get("minLength", 0)
                    max_length = constraints.get("maxLength", float('inf'))
                    if min_length <= len(value) <= max_length:
                        section_data[field] = value
                        break
                    else:
                        print(f"{field.capitalize()} must be between {min_length} and {max_length} characters.")
                elif constraints['bsonType'] == "int":
                    minimum = constraints.get("minimum", float('-inf'))
                    maximum = constraints.get("maximum", float('inf'))
                    value = int(value)
                    if minimum <= value <= maximum:
                        section_data[field] = value
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
        # Insert the new course into the MongoDB collection
        db.sections.insert_one(section_data)
        db.courses.update_one(
            {"course_number": course_number},
            {"$addToSet": {"sections": {"section_number": section_data['section_number'],
                                        "semester": section_data['semester'],
                                        "building": section_data['building'],
                                        "room": section_data['room'],
                                        "instructor": section_data['instructor']}}},
        )
        print("Section added successfully.")
    except pymongo.errors.DuplicateKeyError as e:
        print(f"Error: Section with the same data already exists {e}. Please enter unique section data.")
        add_section(db)  # Re-prompt the user for section data
    except Exception as e:
        print(f"Error: {e}. Please re-enter section data.")
        add_section(db)  # Re-prompt the user for section data


# Function to delete a section
def delete_section(db):
    print("Delete a Section")
    list_section(db)  # List available sections
    if db.sections.count_documents({}) == 0:
        print("No section to delete")
        return
    found = False
    while not found:
        try:
            abbreviation = input("Enter the abbreviation of the section to delete: ").strip().upper()
            course_number = int(input("Enter the course number of the section to delete: "))
            section_number = int(input("Enter the section number of the section to delete: "))
            semester = input("Enter the semester of the section to delete: ")
            section_year = int(input("Enter the section year of the section to delete: "))
            # Check if the section exists
            choose_section = db.sections.find_one(
                {"course_number": course_number, "department_abbreviation": abbreviation,
                 "section_number": section_number, "semester": semester,
                 "section_year": section_year})
            if choose_section:
                # Delete the section
                db.sections.delete_one({"course_number": course_number, "department_abbreviation": abbreviation,
                                        "section_number": section_number, "semester": semester,
                                        "section_year": section_year})
                print("Section deleted successfully.")
                found = True
            else:
                print(f"Section {abbreviation} {course_number} {section_number} {semester} {section_year} not found.")
        except ValueError:
            print(f"Error: Invalid input. Please enter a valid value.")


# Function to list all sections
def list_section(db):
    print("List of sections")
    sections = db.sections.find().sort("section_number")

    for section in sections:
        print(section)


def add_student(db):
    collection = db["students"]
    running = True
    while running:
        try:
            lastName = input("Enter the student last name(max 32 characters): ")
            firstName = input("Enter the student first name(max 32 characters): ")
            email = input("Enter the student's email: ")

            student = {
                "last_name": lastName,
                "first_name": firstName,
                "e_mail": email
            }

            collection.insert_one(student)
            print("Student successfully added.")
        except pymongo.errors.DuplicateKeyError as e:
            print("Error:", e.details['errmsg'])
            print("Please re-enter the student's details.")
            continue
        # except pymongo.errors.WriteError as e:
        #    print("Error:", e.details['errmsg'])
        #    print("Please re-enter the student's details.")
        #    continue
        except Exception as e:
            print("An error occurred:")
            pprint(e)
            print("Please re-enter student's details.")
            continue
        running = False


def select_student(db):
    collection = db["students"]
    found = False
    lastName = ""
    firstName = ""
    while not found:
        lastName = input("Enter the student's last name:")
        firstName = input("Enter the student's first name:")
        name_count = collection.count_documents({"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student


def delete_student(db):
    print("Delete a student")
    all_students = db.students.find()
    for each_student in all_students:
        print(f"Last Name: {each_student['last_name']}, First Name: {each_student['first_name']}")
    student = select_student(db)
    students = db["students"]
    student_id = student.get("_id")
    majors = db["majors"]
    # Check if the student is enrolled in any sections
    enrollment_count = db.enrollments.count_documents({"student_id": student_id})
    if enrollment_count == 0:
        # Remove the student's _id from all majors where they are listed
        majors.update_many({}, {"$pull": {"student_ids": student_id}})

        # Delete the student from the students collection
        deleted = students.delete_one({"_id": student_id})
        print(f"We just deleted: {deleted.deleted_count} students.")
    else:
        print(f"That student is enrolled in {enrollment_count} section(s) \n"
              "You must delete all enrollments before deleting this student.")


def list_student(db):
    students = db["students"].find({}, {"_id": 1, "first_name": 1, "last_name": 1, "e_mail": 1}).sort(
        [("last_name", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING)])
    for student in students:
        pprint(student)


def add_major(db):
    collection = db["majors"]
    department = Department.select_department(db)
    department_id = department.get("_id")
    while True:
        try:
            name = input("Enter Major name:")
            description = input("Enter Major's description")
            major = {
                "department_abbreviation": department.get("abbreviation"),
                "name": name,
                "description": description
            }
            collection.insert_one(major)
            print("Major successfully added.")
            new_department_major = {
                "major_name": name,
                "description": description
            }
            db.departments.update_one(
                {"_id": department_id},
                {"$push": {"majors": new_department_major}}
            )
            break
        except pymongo.errors.DuplicateKeyError as e:
            print("Error:", e.details['errmsg'])
            print("Please re-enter the major's details.")
            continue
        except Exception as e:
            print("An error occurred:")
            pprint(e)
            print("Please re-enter the major's details..")


def select_major(db):
    collection = db["majors"]
    found: bool = False
    name: str = ''
    while not found:
        name = input("Enter Major name:")
        name_count: int = collection.count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No major found by that name. Try again.")
    found_major = collection.find_one({"name": name})
    return found_major


def delete_major(db):
    collection = db["majors"]
    major = select_major(db)
    major_id = major["_id"]

    # Set to track unique student IDs
    unique_student_ids = set()

    # Add IDs from students who have declared this major
    declared_students = db.students.find({"student_major.major_id": major_id}, {"_id": 1})
    for student in declared_students:
        unique_student_ids.add(student["_id"])

    # Add IDs from the major's student_ids array
    enrolled_students = major.get("student_ids", [])
    unique_student_ids.update(enrolled_students)

    total_students = len(unique_student_ids)

    if total_students == 0:
        # If no students are declared or enrolled, delete the major
        db.departments.update_one(
            {"abbreviation": major.get("department_abbreviation")},
            {"$pull": {"majors": {"name": major.get("name")}}}
        )
        deleted = collection.delete_one({"_id": major_id})
        print(f"We just deleted: {deleted.deleted_count} major")
    else:
        print(f"There is a total of {total_students} students enrolled in or declared to this major.\n"
              "They must be removed from the major first before this major may be deleted.")


def list_major(db):
    majors = db["majors"].find({}, {"_id": 1, "department_abbreviation": 1, "name": 1, "description": 1}).sort("name",
                                                                                                               pymongo.ASCENDING)
    for major in majors:
        pprint(major)


def add_student_major(database):
    student_records = database["students"]
    major_records = database["majors"]
    running = True
    while running:
        try:
            selected_student = select_student(database)
            chosen_major = select_major(database)
            major_name_to_check = chosen_major.get("name")
            student_id = selected_student.get("_id")
            major_id = chosen_major.get("_id")

            # Check if the student already has this major
            if major_records.count_documents({"_id": major_id, "student_ids": student_id}) > 0:
                raise Exception(f"Student is already enrolled in the major: {major_name_to_check}")

            current_date = datetime.datetime.now()

            # Add major to student's record
            new_student_major = {
                "major_id": major_id,
                "major_name": major_name_to_check,
                "declaration_date": current_date
            }
            student_records.update_one(
                {"_id": student_id},
                {"$push": {"student_major": new_student_major}}
            )

            # Add student's _id to the major's record
            major_records.update_one(
                {"_id": major_id},
                {"$push": {"student_ids": student_id}}
            )
            print("Major successfully assigned to student")
            running = False
        except Exception as e:
            print("An error occurred:")
            pprint(e)
            print("Please re-enter the major's details..")


def add_major_student(db):
    major_records = db["majors"]
    student_records = db["students"]
    running = True
    while running:
        try:
            chosen_major = select_major(db)
            selected_student = select_student(db)
            major_id = chosen_major.get("_id")
            student_id = selected_student.get("_id")

            # Check if the student already has this major
            if student_records.count_documents({"_id": student_id, "student_major.major_id": major_id}) > 0:
                raise Exception(f"Student is already enrolled in the major: {chosen_major.get('name')}")

            current_date = datetime.datetime.now()

            # Add major to student's record
            new_student_major = {
                "major_id": major_id,
                "major_name": chosen_major.get("name"),
                "declaration_date": current_date
            }
            student_records.update_one(
                {"_id": student_id},
                {"$push": {"student_major": new_student_major}}
            )

            # Add student's _id to the major's record
            major_records.update_one(
                {"_id": major_id},
                {"$push": {"student_ids": student_id}}
            )
            print("Major successfully assigned to student")
            running = False
        except Exception as e:
            print("An error occurred:")
            pprint(e)
            print("Please re-enter the major's details.")
            continue


def select_major_student(db):
    collection = db["students"]
    found = False
    student = select_student(db)
    while not found:
        major = select_major(db)
        student_major_count: int = collection.count_documents({"_id": student.get("_id"),
                                                               "student_major": {
                                                                   "$elemMatch": {"major_name": major.get("name")}}})
        found = student_major_count == 1
        if not found:
            print("No student major found was found. Try again.")
    found_student = collection.find_one({"_id": student.get("_id"),
                                         "student_major": {"$elemMatch": {"major_name": major.get("name")}}})
    return found_student


def select_student_major(db, major_id):
    collection = db["students"]
    while True:
        student = select_student(db)
        student_id = student["_id"]

        # Check if the student is enrolled in the selected major
        student_major_count = collection.count_documents(
            {"_id": student_id, "student_major": {"$elemMatch": {"major_id": major_id}}}
        )

        if student_major_count == 1:
            return student
        else:
            print("No student major found was found. Try again.")


def delete_student_major(db):
    student_major = select_major_student(db)
    if student_major:
        student_id = student_major["_id"]
        major_id = student_major["student_major"][0]["major_id"]

        # Update student's record
        db.students.update_one(
            {"_id": student_id},
            {"$pull": {"student_major": {"major_id": major_id}}}
        )

        # Remove student's _id from the major's record
        db.majors.update_one(
            {"_id": major_id},
            {"$pull": {"student_ids": student_id}}
        )
        print("Deleted student major successfully")


def delete_major_student(db):
    chosen_major = select_major(db)
    major_id = chosen_major["_id"]

    selected_student = select_student_major(db, major_id)
    if selected_student:
        student_id = selected_student["_id"]

        # Update student's record
        db.students.update_one(
            {"_id": student_id},
            {"$pull": {"student_major": {"major_id": major_id}}}
        )

        # Remove student's _id from the major's record
        db.majors.update_one(
            {"_id": major_id},
            {"$pull": {"student_ids": student_id}}
        )
        print("Deleted student major successfully")


def list_major_student(db):
    major_collection = db["majors"]
    student_collection = db["students"]
    query = {}  # Empty query to fetch all majors
    sorting_order = [("name", pymongo.ASCENDING)]  # Sort by major name
    all_majors = major_collection.find(query).sort(sorting_order)

    for major in all_majors:
        display_info = {
            "Major Name": major.get('name'),
            "Department Abbreviation": major.get('department_abbreviation')
        }
        pprint(display_info)

        # Fetching students who declared this major
        student_ids = major.get('student_ids', [])
        if student_ids:
            print("Students:")
            for student_id in student_ids:
                student = student_collection.find_one({"_id": student_id})
                if student:
                    student_info = {
                        "Student Name": student.get('first_name') + " " + student.get('last_name')
                    }
                    pprint(student_info)
            print()


def list_student_major(db):
    student_collection = db["students"]
    query = {}  # Empty query to fetch all students
    sorting_order = [("last_name", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING)]
    all_students = student_collection.find(query).sort(sorting_order)

    for student in all_students:
        display_info = {
            "Name": student.get('first_name') + " " + student.get('last_name')
        }
        pprint(display_info)

        declared_majors = student.get('student_major', [])
        if declared_majors:
            print("Majors:")
            for major in declared_majors:
                pprint({
                    "Major Name": major.get("major_name"),
                    "Declaration Date": major.get("declaration_date")
                })
            print()


# Enrollment
def select_section(db):
    out = False
    while not out:
        department_abbreviation = input("Enter department abbreviation: ")
        course_number = input("Enter course number: ")
        section_number = input("Enter section number: ")
        semester = input("Enter semester: ")
        section_year = input("Enter section year: ")
        try:
            course_number = int(course_number)
            section_number = int(section_number)
            section_year = int(section_year)
        except ValueError:
            print("Course number and section number must be integers. Please try again.")
            continue

        section = db.sections.find_one({
            "department_abbreviation": department_abbreviation,
            "course_number": course_number,
            "section_number": section_number,
            "semester": semester,
            "section_year": section_year,
        })

        if section:
            return section
        else:
            choose = input("Section not found. Please try again by press enter. Or type 'exit' to exit: ")
            if choose == "exit":
                return 0


def add_student_PassFail(db):
    section_records = db["sections"]
    student_records = db["students"]
    running = True
    while running:
        student = select_student(db)
        section = select_section(db)
        if student == 0 or section == 0:
            return
        elif not student or not section:
            print("Invalid student or section. Please try again.")
            continue

        if db.enrollments.find_one({"student_id": student["_id"], "section_id": section["_id"]}):
            print("Student already in this section. Try again.")
        elif db.enrollments.find_one({"student_id": student["_id"], "semester": section["semester"],
                                      "section_year": section["section_year"],
                                      "department_abbreviation": section["department_abbreviation"],
                                      "course_number": section["course_number"]}):
            print("Student already enrolled this section in this semester. Try again.")
        else:
            current_date = datetime.datetime.now()
            pass_fail_document = {
                "student_id": student["_id"],
                "section_id": section["_id"],
                "last_name": student["last_name"],
                "first_name": student["first_name"],
                "department_abbreviation": section["department_abbreviation"],
                "course_number": section["course_number"],
                "section_number": section["section_number"],
                "semester": section["semester"],
                "section_year": section["section_year"],
                "enrollment_category_data": {
                    "type": "PassFail",
                    "application_date": current_date
                }
            }
            db.enrollments.insert_one(pass_fail_document)
            student_records.update_one(
                {"_id": student["_id"]},
                {"$addToSet": {"enrollment_courses": {"section_id": section["_id"],
                                                      "department_abbreviation": section["department_abbreviation"],
                                                      "course_number": section["course_number"],
                                                      "section_number": section["section_number"],
                                                      "building": section["building"],
                                                      "room": section["room"], "start_hour": section["start_hour"],
                                                      "start_minute": section["start_minute"],
                                                      "instructor": section["instructor"]}}},
            )
            section_records.update_one(
                {"_id": section["_id"]},
                {"$addToSet": {"enrollment_students": {"student_id": student["_id"]}}},
            )
            print("Student enrolled as PassFail.")
            running = False


def add_student_LetterGrade(db):
    section_records = db["sections"]
    student_records = db["students"]
    running = True
    while running:
        student = select_student(db)
        section = select_section(db)
        if student == 0 or section == 0:
            return
        if db.enrollments.find_one({"student_id": student["_id"], "section_id": section["_id"]}):
            print("Student already enrolled in this section. Try again.")
        elif db.enrollments.find_one({"student_id": student["_id"], "semester": section["semester"],
                                      "section_year": section["section_year"],
                                      "department_abbreviation": section["department_abbreviation"],
                                      "course_number": section["course_number"]}):
            print("Student already enrolled this section in this semester. Try again.")
        else:
            while True:
                min_acceptable = input("Please enter minimum acceptable Letter grade (A or B or C)--> ")
                if min_acceptable.upper() == 'A' or min_acceptable.upper() == "B" or min_acceptable.upper() == "C":
                    break
            letter_grade_document = {
                "student_id": student["_id"],
                "section_id": section["_id"],
                "last_name": student["last_name"],
                "first_name": student["first_name"],
                "department_abbreviation": section["department_abbreviation"],
                "course_number": section["course_number"],
                "section_number": section["section_number"],
                "semester": section["semester"],
                "section_year": section["section_year"],
                "enrollment_category_data": {
                    "type": "LetterGrade",
                    "min_satisfactory": min_acceptable
                }

            }
            db.enrollments.insert_one(letter_grade_document)
            student_records.update_one(
                {"_id": student["_id"]},
                {"$addToSet": {"enrollment_courses": {"section_id": section["_id"],
                                                      "department_abbreviation": section["department_abbreviation"],
                                                      "course_number": section["course_number"],
                                                      "section_number": section["section_number"],
                                                      "building": section["building"],
                                                      "room": section["room"], "start_hour": section["start_hour"],
                                                      "start_minute": section["start_minute"],
                                                      "instructor": section["instructor"]}}},
            )
            section_records.update_one(
                {"_id": section["_id"]},
                {"$addToSet": {"enrollment_students": {"student_id": student["_id"]}}},
            )
            print("Student enrolled as LetterGrade.")
            running = False


def delete_student_section(db):
    running = True
    while running:
        student = select_student(db)
        if not student:
            print("Invalid student. Please try again.")
            continue

        section = select_section(db)
        if not section:
            print("Invalid section. Please try again.")
            continue

        # Find and delete the enrollment
        result = db.enrollments.delete_one({"student_id": student["_id"], "section_id": section["_id"]})
        if result.deleted_count > 0:
            try:
                db.students.update_one(
                    {"_id": student["_id"]},
                    {"$pull": {"enrollment_courses": {"section_id": section["_id"]}}}
                )
                db.sections.update_one(
                    {"_id": section["_id"]},
                    {"$pull": {"enrollment_students": {"student_id": student["_id"]}}}
                )
                print("Enrollment successfully deleted.")
                running = False
            except Exception as e:
                print(f"Error updating students/sections: {e}")
        else:
            print("No enrollment found for this student in the section. Try again.")


def delete_section_student(db):
    running = True
    while running:
        section = select_section(db)
        if not section:
            print("Invalid section. Please try again.")
            continue

        student = select_student(db)
        if not student:
            print("Invalid student. Please try again.")
            continue

        # Find and delete the enrollment
        result = db.enrollments.delete_one({"student_id": student["_id"], "section_id": section["_id"]})
        if result.deleted_count > 0:
            try:
                db.students.update_one(
                    {"_id": student["_id"]},
                    {"$pull": {"enrollment_courses": {"section_id": section["_id"]}}}
                )
                db.sections.update_one(
                    {"_id": section["_id"]},
                    {"$pull": {"enrollment_students": {"student_id": student["_id"]}}}
                )
                print("Enrollment successfully deleted.")
                running = False
            except Exception as e:
                print(f"Error updating students/sections: {e}")
        else:
            print("No enrollment found for this student in the section. Try again.")


def list_enrollment(db):
    enrollments = db.enrollments.find({}, {"last_name": 1, "first_name": 1})

    for enrollment in enrollments:
        print(f"Last Name: {enrollment['last_name']}, First Name: {enrollment['first_name']}")

    running = True
    while running:
        student = select_student(db)
        if not student:
            print("Invalid student. Please try again.")
            continue
        student_chose = list(db.enrollments.find({"student_id": student["_id"]}))
        if not student_chose:
            print(f"No course enrollments found for that student.")
        else:
            for enrollment in student_chose:
                print(
                    f"Course: {enrollment['course_number']}, Section: {enrollment['section_number']}, "
                    f"Semester: {enrollment['semester']}")
                running = False
# def course_completion_status(db):
#     student = select_student(db)
#
#     department_abbreviation = input("Enter department abbreviation: ")
#     course_number = input("Enter course number: ")
#     section_number = input("Enter section number: ")
#     semester = input("Enter semester: ")
#     section_year = input("Enter section year: ")
#
#     try:
#         course_number = int(course_number)
#         section_number = int(section_number)
#         section_year = int(section_year)
#     except ValueError:
#         print("Course number, section number, and section year must be integers.")
#         return
#
#     completion_status = input("Has the student completed the course? (Yes/No): ").strip().lower()
#     if completion_status not in ["yes", "no"]:
#         print("Invalid input. Please enter 'Yes' or 'No'.")
#         return
#
#     # Map user input to a status
#     status = "Completed" if completion_status == "yes" else "Incomplete"
#
#     # Find and update the completion status
#     result = db.completion_statuses.update_one(
#         {
#             "student_id": student["_id"],
#             "department_abbreviation": department_abbreviation,
#             "course_number": course_number,
#             "section_number": section_number,
#             "semester": semester,
#             "section_year": section_year
#         },
#         {"$set": {"completion_status": status}}
#     )
#
#     if result.matched_count > 0:
#         print("Course completion status updated successfully.")
#     else:
#         print("No matching record found or no update was needed.")


def boilerplate(db):
    preload_departments = [
        {
            "name": "Computer Science",
            "abbreviation": "CECS",
            "chair_name": "John Smith",
            "building": "ECS",
            "office": 123,
            "description": "Computer Science",
        },
        {
            "name": "Biology Department",
            "abbreviation": "BIO",
            "chair_name": "Sarah Johnson",
            "building": "VEC",
            "office": 111,
            "description": "Biology",  #
        },
        {
            "name": "Physics Department",
            "abbreviation": "PHY",
            "chair_name": "Robert Davis",
            "building": "EN2",
            "office": 222,
            "description": "Physics Department",
        },
    ]
    preload_courses = [
        {
            "department_abbreviation": "CECS",
            "course_number": 323,
            "course_name": "Database",
            "description": "MongoDB and SQL",
            "units": 3
        },
        {
            "department_abbreviation": "CECS",
            "course_number": 329,
            "course_name": "Concepts Computer Sci Theory",
            "description": "Concepts Computer Sci Theory",
            "units": 3
        },
        {
            "department_abbreviation": "BIO",
            "course_number": 315,
            "course_name": "Bio and Chem",
            "description": "Bio and Chem",
            "units": 4
        },
    ]

    for department_data in preload_departments:
        if all(field in department_data for field in Department.department_schema['$jsonSchema']['required']):
            # Check if the department data includes all required fields
            db.departments.insert_one(department_data)
        else:
            print("Invalid department data. Make sure it includes all required fields.")

    for course_data in preload_courses:
        if all(field in course_data for field in Course.course_schema['$jsonSchema']['required']):
            # Check if the department data includes all required fields
            db.courses.insert_one(course_data)
        else:
            print("Invalid course data. Make sure it includes all required fields.")


if __name__ == '__main__':
    main_action: str = ''
    while main_action != menu_definitions.menu_main.last_action():
        main_action = menu_definitions.menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
