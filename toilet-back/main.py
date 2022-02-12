from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime

client = MongoClient('mongodb://localhost', 27017)

app = FastAPI()

db = client["mini-project"]
collection = db["room"]


@app.post("/start/{room_number}")
def start(room_number: int):
    now = datetime.now()
    collection.insert_one({
        "room": room_number,
        "empty": 0,
        "start": now.strftime("%Y-%m-%d %H:%M:%S"),
        "end": None,
        "total_time": None
    })
    return {
        "msg": f"{room_number} is currently in use"
    }


@app.post("/end/{room_number}")
def end(room_number: int):
    now = datetime.now()

    room = collection.find({"room": room_number}).sort("_id", -1)[0]

    collection.update_one(
            {
                "room": room_number,
                "start": room["start"]
            }, 
            {
                "$set": {
                    "end": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "total_time": (now - datetime.strptime(room["start"], "%Y-%m-%d %H:%M:%S")).total_seconds()
                }
            }
        )

    return {
        "msg": f"{room_number} is empty"
    }