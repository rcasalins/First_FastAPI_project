from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post("/")
async def post():
    return {'message': 'Welcome to the post route'}

@app.put("/")
async def put():
    return {'message': 'Welcome to the post route'}

@app.get('/users')
async def list_users():
    return {'message': 'list iusers route'}

@app.get('/users/me')
async def get_users():
    return {'message': 'this is the current user'}

@app.get('/users/{users_id}')
async def get_users(users_id: int):
    return {'users_id': users_id}

class FoodEnum(str, Enum):
    fruits = 'Fruits'
    vegetables = 'Vegetables'
    dairy = 'Dairy'

@app.get('/foods/{food_name}')
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {'food_name': food_name, 'message': 'You are heathy'}

    if food_name.value == "Fruits":
        return {'food_name': food_name, 'message': 'You are heathy, but dumbas'}

    return {'food_name': food_name, 'message': 'I like you, have a cake'}


fake_items_db = [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]

@app.get('/items')
async def list_items(skip: int=0, limit: int=10):
    return fake_items_db[skip: skip + limit]

@app.get('/items/{item_id}')
async def get_item(item_id: str, q: str | None = None, short: bool=False):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    
    if not short:
        item.update({
            'description': 'Lorem ipsum'
        })
    return item

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post('/items')
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'Price with tax': price_with_tax})
    return item_dict

# @app.put('/items')
