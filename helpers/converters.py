from bson import ObjectId
from fastapi.encoders import jsonable_encoder

def convert_objectid(data):
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    if isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    return data
