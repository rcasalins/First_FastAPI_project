#from typing import Union
import json
from fastapi import FastAPI, Query, Path
from starlette.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from fastapi import FastAPI

app = FastAPI()

@app.middleware('http')
async def user_agent(request: Request, call_next):
    if request.headers['User-Agent'].find('Mobile') == -1:
        response = await call_next(request)
        return response
    else:
        return JSONResponse(content = {'message': 'Do not use a fucking mobile'}, status_code = 401)

DB = {}

@app.post('/')
def root():
    return DB

class User(BaseModel):
    password: str

@app.put('/{user_id}')
async def user_put(user_id: str, passw: User):
    json_compatible_item_data = jsonable_encoder(passw)
    DB[user_id] = json_compatible_item_data
    return DB

@app.get('/verification/{user}')
async def user_validation(user: str, password: str):
    result = 'Active'
    if DB.get(user):
        if DB[user] == {'password': password}:

            return result

    return JSONResponse(content = {'message': 'User or password wrong'}, status_code = 401)

@app.delete('/delete/{user}')
async def user_delete(user: str):
    if DB.get(user):
        del DB[user]
    else:
        return JSONResponse(content = {'message': 'User or password wrong'}, status_code = 401)

    return DB
