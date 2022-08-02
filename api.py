from fastapi import FastAPI

# from typing import Optional
# from pydantic import BaseModel
from db.controls import fetchall, insert_data
import json
import pprint

app = FastAPI()


@app.get("/")
async def root():
    db_data = fetchall()
    return {"Objects": db_data}


@app.post("/post/")
async def create_item(name, price, tax, des="none"):
    if not name or len(name) < 3:
        return {"message": "Name must be > 3"}
    if not price:
        return {"message": "Fields must not be blank."}
    if not tax:
        return {"message": "Fields must not be blank."}
    get_res = insert_data(name=name, des=des, price=price, tax=tax)
    if get_res:
        return {"message": get_res}
    return {"message": "failed"}
