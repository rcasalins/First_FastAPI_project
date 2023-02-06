#from typing import Union
from fastapi import FastAPI, Query
from starlette.requests import Request
from fastapi.responses import JSONResponse

from fastapi import FastAPI

app = FastAPI()

@app.middleware('http')
async def user_agent(request: Request, call_next):
    if request.headers['User-Agent'].find('Mobile') == -1:
        response = await call_next(request)
        return response
    else:
        return JSONResponse(content = {'message': 'Do not use a fucking mobile'}, status_code = 401)

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

@app.get('/')
def root():
    return {'message': 'Hello World'}