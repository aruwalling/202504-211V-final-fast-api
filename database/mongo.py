from pymongo import MongoClient
from pymongo.collection import Collection
from models.student import StudentCreate, StudentUpdate
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()



MONGO_URI = os.getenv("MONGO_URL")
DATABASE_NAME = "final_db"
COLLECTION_NAME = "students"



client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


def initialize_students_collection():
    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "dni",
                "name",
                "age",
                "grade",
                "is_approved",
                "created_at",
                "updated_at"
            ],
            "properties": {
                "dni": {
                    "bsonType": "string",
                    "minLength": 8,
                    "maxLength": 8,
                    "description": "DNI is required and must have 8 characters"
                },
                "name": {
                    "bsonType": "string",
                    "minLength": 1,
                    "description": "Name is required"
                },
                "age": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "Age is required and must be greater than or equal to 0"
                },
                "grade": {
                    "bsonType": ["double", "int"],
                    "minimum": 0,
                    "maximum": 20,
                    "description": "Grade must be between 0 and 20"
                },
                "is_approved": {
                    "bsonType": "bool",
                    "description": "Approval status is required"
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Creation timestamp is required"
                },
                "updated_at": {
                    "bsonType": "date",
                    "description": "Update timestamp is required"
                }
            }
        }
    }

    if COLLECTION_NAME not in db.list_collection_names():
        db.create_collection(
            COLLECTION_NAME,
            validator=validator,
            validationLevel="strict",
            validationAction="error"
        )
    else:
        db.command({
            "collMod": COLLECTION_NAME,
            "validator": validator,
            "validationLevel": "strict",
            "validationAction": "error"
        })

    students_collection = db[COLLECTION_NAME]

    students_collection.create_index("dni", unique=True)


initialize_students_collection()

students_collection: Collection = db[COLLECTION_NAME]

def map_student(student):
    student["id"]=str(student.pop("_id"))
    return student

def create_student(student: StudentCreate) -> dict:
    now = datetime.now(timezone.utc)

    student_data = student.model_dump()
    student_data["created_at"] = now
    student_data["updated_at"] = now

    students_collection.insert_one(student_data)
    map_student(student_data)

    return student_data


def get_all_students() -> list[dict]:
    return [map_student(student) for student in students_collection.find({})]


def get_student_by_id(student_id: ObjectId) -> dict | None:
    student = students_collection.find_one(
        {"_id": student_id}
    )
    if student:
        map_student(student)
    return student


def update_student(student_id: ObjectId, student: StudentUpdate) -> dict | None:
    update_data = student.model_dump(exclude_unset=True)

    if not update_data:
        return get_student_by_id(student_id)

    update_data["updated_at"] = datetime.now(timezone.utc)

    result = students_collection.update_one(
        {"_id": student_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return None

    return get_student_by_id(student_id)


def delete_student(student_id: ObjectId) -> bool:
    result = students_collection.delete_one({"_id": student_id})
    return result.deleted_count > 0


def create_students_bulk(students: list[StudentCreate]) -> list[dict]:
    created_students = []

    for student in students:
        created_students.append(create_student(student))

    return created_students