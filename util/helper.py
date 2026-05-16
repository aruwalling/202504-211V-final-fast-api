from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError
from bson import ObjectId


def parse_objectid(student_id):
    try:
        student_id = ObjectId(student_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El indentificador deberia ser un ObjectID")
    return student_id