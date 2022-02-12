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
        "done": 0,
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
                    "done": 1,
                    "end": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "total_time": (now - datetime.strptime(room["start"], "%Y-%m-%d %H:%M:%S")).total_seconds()
                }
            }
        )

    return {
        "msg": f"{room_number} is empty"
    }

@app.get("/room-status/{room_number}")
def room_status(room_number: int):
    room = collection.find({"room": room_number}).sort("_id", -1)[0]
    
    return {
        "room": room["room"],
        "done": room["done"],
        "start": room["start"],
        "end": room["end"],
        "total_time": room["total_time"]
    }

@app.get("/estimate")
def estimate():
    """Average time of all completed session in seconds."""
    room = collection.find({"done": 1})

    total_time = 0
    count = 0
    for r in room:
        total_time += r["total_time"]
        count += 1

    return {
        "estimate": total_time / count,
        "completed_session": count
    }