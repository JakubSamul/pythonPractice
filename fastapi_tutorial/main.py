from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Form,
    Header,
    Query,
    Path,
    Body,
    status,
    File,
    UploadFile,
    HTTPException,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "hello world"}


# @app.post("/")
# async def post():
#     return {"message": "hello from the post route"}


# @app.put("/")
# async def get():
#     return {"message": "hello from the put route"}


# @app.get("/users")
# async def list_users():
#     return {"message": "list users route"}


# @app.get("/users/me")
# async def get_current_user():
#     return {"message": "this is the current user"}


# @app.get("/users/{user_id}")
# async def get_user(user_id: str):
#     return {"user_id": user_id}

# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegetables = "vegetables"
#     dairy = "dairy"


# @app.get("/food/{food_name}")
# async def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {
#             "food_name": food_name,
#             "message": "you are healthy"
#         }

#     if food_name.value == "fruits":
#         return {
#             "food_name": food_name,
#             "message": "you are still healthy, but like sweet things"
#         }
#     return {
#         "food_name": food_name,
#         "message": "I like chocolate milk"
#     }


# fake_items_db = [
#     {"item_name": "Foo"},
#     {"item_name": "Bar"},
#     {"item_name": "Baz"}
#     ]

# @app.get("/items")
# async def list_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# @app.get("/items/{item_id}")
# async def get_item(item_id: str, sample_query_param: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id, "sample_query_param": sample_query_param}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {
#                 "description": "blaa blaa blaa"
#             }
#         )
#     return item


# @app.get("/users/{user_id}/items/{item_id}")
# async def get_user_id(user_id: int, item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id, "user_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {
#                 "description": "blaa blaa blaa"
#             }
#         )
#     return item


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.post("/items")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


# @app.put("/items/{item_id}")
# async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result


# @app.get("/items")
# async def read_items(
#     q: str
#     | None = Query(
#         None,
#         min_length=3,
#         max_length=10,
#         title="Sample query string",
#         description="This is a sample query string.",
#         alias="item-query",
#     )
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/items_hidden")
# async def hidden_query_route(
#     hidden_query: str | None = Query(None, include_in_schema=False)
# ):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     return {"hidden_query": "Not found"}


# @app.get("/items_validation/{item_id}")
# async def resd_items_validation(*, item_id: int = Path(..., title="The ID of the item to gey", gt=10, lt=100), q: str = "hello", size: float = Query(..., gt=0, lt=7.75)):
#     result = {"item_id": item_id, "size": size}
#     if q:
#         result.update({"q": q})
#     return result

# part 7 Body -> Multiple parameters
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# class User(BaseModel):
#     username: str
#     full_name: str | None = None


# app.put("/items/{item_id}")
# async def update_item(
#         *,
#         item_id: int = Path(..., title="The ID of the item to get", ge=0, le=150),
#         q: str | None = None,
#         item: Item = Body(..., embed=True)
# ):
#     result = {"item_id": item_id}
#     if q:
#         result.update({"q": q})
#     if item:
#         result.update({"item": item})
#     return result

# Part 8 -> Body -> Field
# class Item(BaseModel):
#     name: str
#     description: str | None = Field(None, title="The description of the item", max_length=300)
#     price: float = Field(..., gt=0, description="The price must be greater than zero.")
#     tax: float | None = None

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(..., embed=True)):
#     result = {"item_id": item_id, "item": item}
#     return result

# Part 9 -> Body -> Nasted Models
# class Image(BaseModel):
#     url: HttpUrl
#     name: str


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = []
#     image: Image | None = None


# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     item: list[Item]


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     result = {"item_id": item_id, "item": item}
#     return result


# @app.post("/offers")
# async def cretae_offer(offer: Offer = Body(..., embed=True)):
#     return offer


# @app.post("/images/multiple")
# async def create_multiple_images(images: list[Image]):
#     return images


# @app.post("/blah")
# async def create_some_blahs(blahs: dict[int, float]):
#     return blahs

#  Part 10 -> Declare Request Example Data
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

#     # class Confg:
#     #     schema_extra = {
#     #         "example": {
#     #             "name": "foo",
#     #             "description": "A very nice item",
#     #             "price": 16.25,
#     #             "tax": 1.67,
#     #         }
#     #     }


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Item = Body(
#         ...,
#         examples={
#             "normal": {
#                 "summary": "A normal example",
#                 "description": "A normal item work correctly",
#                 "value": {
#                     "name": "Foo",
#                     "description": "This is a nice item",
#                     "price": 16.25,
#                     "tax": 1.67,
#                 },
#             },
#             "converted": {
#                 "summary": "An example with converted data",
#                 "description": "FastAPI can convert price 'string' to actual 'number'",
#                 "value": {"name": "Bar", "price": "16.25"},
#             },
#             "invalid": {
#                 "summary": "Invalid data is rejected with an error",
#                 "value": {"name": "Baz", "price": "sixteen point two five"},
#             },
#         },
#     ),
# ):
#     result = {"item_id": item_id, "item": item}
#     return result

# Part 11 -> Extra Data Types
# @app.put("/items/{item_id}")
# async def read_items(item_id: UUID, start_date: datetime | None = Body(None), end_date: datetime | None = Body(None), repeat_at: time | None = Body(None), process_after: timedelta | None = Body(None)):
#     start_process = start_date + process_after
#     duration = end_date - start_process
#     return {
#         "item_id": item_id,
#         "start_date": start_date,
#         "end_date": end_date,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }

# Part 12 -> Cookie and Header Parameters
# @app.get("/items")
# async def read_items(
#     cookie_id: str | None = Cookie(None),
#     accept_encoding: str | None = Header(None),
#     sec_ch_ua: str | None = Header(None),
#     user_agent: str | None = Header(None),
#     x_token: list[str] | None = Header(None),
# ):
#     return {
#         "cookie_id": cookie_id,
#         "Accept-Encoding": accept_encoding,
#         "sec-ch-ua": sec_ch_ua,
#         "User-Agent": user_agent,
#         "X-Token value": x_token,
#     }

# Part 13 -> Response MOdel
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5
#     tags: list[str] = []


# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }


# @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]


# @app.post("/items/", response_model=Item)
# async def create_item(item: Item):
#     return item


# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# class UserIn(BaseModel):
#     password: str


# class UserOut(BaseModel):
#     pass


# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn):
#     return user


# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include={"name", "descripion"},
# )
# async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]


# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
# async def read_item_public_data(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]

# Part 14 -> Extra Models
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     fll_name: str | None = None


# class UserIn(UserBase):
#     password: str


# class UserOut(UserBase):
#     pass


# class UserInDB(UserBase):
#     hashed_password: str


# def fake_password_hasher(raw_password: str):
#     return f"supersecret{raw_password}"


# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("User 'saved'.")
#     return user_in_db


# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved


# class BaseItem(BaseModel):
#     description: str
#     type: str


# class CarItem(BaseItem):
#     type = "car"


# class PlaneItem(BaseItem):
#     type = "plane"
#     size: int


# items = {
#     "item1": {"description": "Bla bla bla", "type": "car"},
#     "item2": {"description": "Bu buuu buuuuuu", "type": "plane", "size": 8},
# }


# @app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
# async def read_item(item_id: Literal["item1", "item2"]):
#     return items[item_id]


# class ListItem(BaseModel):
#     name: str
#     description: str


# list_items = [
#     {"name": "Foo", "description": "there bla bla"},
#     {"name": "Red", "description": "Bu bla da"}
# ]


# @app.get("/list_items/", response_model=list[ListItem])
# async def read_items():
#     return items


# @app.get("/arbitrary", response_model=dict[str, float])
# async def get_arbitrary():
#     return {"foo": 1, "bar": "bar"}


# 15 - Response Status Code
# @app.post("/item/", status_code=status.HTTP_201_CREATED)
# async def create_item(name: str):
#     return {"name": name}


# @app.delete("/item/{pk}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_item(pk: str):
#     print("pk", pk)
#     return pk


# @app.get("/item/", status_code=status.HTTP_302_FOUND)
# async def read_items_redirect():
#     return {"hello": "world"}


#  16 - From Fields
# @app.post("/login/")
# async def login(username: str = Form(...), password: str = Form(...)):
#     print("password", password)
#     return {"username": username}


# @app.post("/login-json/")
# async def login_json(username: str = Body(...), password: str = Body(...)):
#     print("password", password)
#     return {"username": username}


# 17 - Request Files
# @app.post("/files/")
# async def create_file(files: list[bytes] = File(..., description="A file read as bytes")):
#     return {"file_size": [len(file) for file in files]}

# @app.post("/uploadfiles/")
# async def create_upload_file(files: list[UploadFile] = File(..., description="A file read as UploadFile")):
#     return {"filename": [file.filename for file in files]}


# 18 - Request Forms and Files
# @app.post("/files/")
# async def create_file(file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...), hello: str = Body(...)):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#         "hello": hello,
#     }


# # 19 Handling Errors
# items = {'foo': 'The Foo Wrestlers'}


# @app.get('/items/{items_id}')
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail='Item not found', headers={'X-Error': 'There goes my error'})
#     return {'item': items[item_id]}


# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name


# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(status_code=418, content={'message': f"Oops! {exc.name} did something. There goes a rainbow..."},)


# @app.get('/unicorns/{name}')
# async def read_unicorns(name: str):
#     if name == 'yolo':
#         raise UnicornException(name=name)
#     return {'unicorn_name': name}


# # @app.exception_handler(RequestValidationError)
# # async def validation_exception_handler(request, exc):
# #     return PlainTextResponse(str(exc), status_code=400)


# # @app.exception_handler(StarletteHTTPException)
# # async def http_exception_handler(request, exc):
# #     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# # @app.get('/valodation_item/{item_id}')
# # async def read_validation_items(item_id: int):
# #     if item_id == 3:
# #         raise HTTPException(status_code=418, detail='Nope! I dont like 3.')
# #     return {'item_id': item_id}


# # @app.exception_handler(RequestValidationError)
# # async def validation_exception_handler(request: Request, exc: RequestValidationError):
# #     return JSONResponse(
# #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
# #         content=jsonable_encoder({'detail': exc.errors(), 'blahblah': exc.body}),
# #     )


# # class Item(BaseModel):
# #     title: str
# #     size: int


# # @app.post('/item/')
# # async def create_item(item: Item):
# #     return item


# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f"OMG: The client sent invalid data!: {exc}")
#     return await http_exception_handler(request, exc)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print(f"OMG: The client sent invalid data!: {exc}")
#     return await request_validation_exception_handler(request, exc)


# @app.get('/blah_items/{item_id})')
# async def read_items(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail='Nope! I dont like 3.')
#     return {'item_id': item_id}


# # 20 - Path Operation Configuration
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()

# class Tags(Enum):
#     items = 'items'
#     users = 'users'


# @app.post(
#     '/items/',
#     response_model=Item,
#     status_code=status.HTTP_201_CREATED,
#     tags=[Tags.items],
#     summary='Create an Item-type item',
#     # description='Create an item with all the information:'
#     # 'name; description; price; tax; and a set of '
#     # 'unique tags',
#     response_description='The create item',
# )
# async def create_item(item: Item):
#     """
#     Create an item with all the information:

#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesnt have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item


# @app.get('/items/', tags=[Tags.items])
# async def read_items():
#     return [{'name': 'Foo', 'price': 42}]


# @app.get('/users/', tags=[Tags.users])
# async def read_users():
#     return [{'username': 'JakubSamul'}]


# @app.get('/elements/', tags=[Tags.items], deprecated=True)
# async def read_elements():
#     return [{'item_id': 'Foo'}]


# # 21 - JSON Compatible Encoder
# class Item(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
#     tax: float = 10.5
#     tags: list[str] = []


# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {
#         "name": "Baz",
#         "description": None,
#         "price": 50.2,
#         "tax": 10.5,
#         "tags": [],
#     },
# }


# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items.get(item_id)


# @app.put("/items/{id}", response_model=Item)
# def update_item(item_id: str, item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     return update_item_encoded


# @app.patch("/items/{item_id}", response_model=Item)
# def patch_item(item_id: str, item: Item):
#     stored_item_data = items.get(item_id)
#     if stored_item_data is not None:
#         stored_item_data = Item(**stored_item_data)
#     else:
#         stored_item_model = Item()
#     update_data = item.dict(exclude_unset=True)
#     update_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(update_item)
#     return update_item


# # 22 - Dependencies Intro
# async def hello():
#     return "world"


# async def comon_parameters(
#     q: str | None = None, skip: int = 0, limit: int = 100, blah: str = Depends(hello)
# ):
#     return {"q": q, "skip": skip, "limit": limit, "hello": blah}


# @app.get("/items/")
# async def read_items(commons: dict = Depends(comon_parameters)):
#     return commons


# @app.get("/users/")
# async def read_users(commons: dict = Depends(comon_parameters)):
#     return commons


# 23 - Classes as Dependencies
# fake_items_db = [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]


# class ComonQueryParams:
#     def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit

    
# @app.get('/items/{item_id}')
# async def read_items(commons: ComonQueryParams = Depends()):
#     response = {}
#     if commons.q:
#         response.update({'q': commons.q})
#     items = fake_items_db[commons.skip: commons.skip + commons.limit]
#     response.update({'items': items})
#     return response 


# 24 - Sub-Dependencies
# def query_extractor(q: str | None = None):
#     return q 


# def query_or_body_extractor(q: str = Depends(query_extractor), last_query: str | None = Body(None)):
#     if not q:
#         return last_query
#     return q


# @app.post('/item')
# async def try_query(query_or_body: str = Depends(query_or_body_extractor)):
#     return {'q_or_body': query_or_body}


# 25 - Dependencies in path operation decorators
# async def verify_token(x_token: str = Header(...)):
#     if x_token != 'fake-super-secret-token':
#         raise HTTPException(status_code=400, detail='X-Token header invalid')
    

# async def verify_key(x_key: str = Header(...)):
#     if x_key != 'fake-super-secret-key':
#         raise HTTPException(status_code=400, detail='X-Key header invalid')
#     return x_key


# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


# @app.get('/items')
# async def reaf_items():
#     return [{'item': 'Foo'}, {'item': 'Bar'}]


# @app.get('/users')
# async def reaf_users():
#     return [{'username': 'Jakub'}, {'username': 'Basia'}]


# 26 - Security, First Step
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl ='token')

# fake_users_db = {
#     'johndoe': dict(
#         username='johndoe',
#         full_name='John Doe',
#         email='johndoe@example.com',
#         hashed_password='fakehashedsecred',
#         disable=False,
#     ),
#     'alice': dict(
#         username='alice',
#         full_name='Alice Wonderson',
#         email='alice@example.com',
#         hashed_password='fakehashedsecred2',
#         disable=False,
#     ),
# }


# def fake_hash_password(password: str):
#     return f'fakehashed{password}'


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
    

# def fake_decode_token(token):
#     return get_user(fake_users_db, token)


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Invalid authentication credentials',
#             headers={'WWW-Authenticate': 'Bearer'},
#         )
#     return user

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail='Inactive user')
#     return current_user


# @app.post('/token')
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail='Incorrect username or password')
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail='Incorrect username or password')
#     return {'access_token': user.username, 'token_type': 'bearer'}


# @app.get('/users/me')
# async def get_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


#  27 - Security, OAuth2 Bearer and JWT
# SECRET_KEY = 'thequickbrownfoxjumpsoverthelazydog'
# ALGOTITHM = 'HS256'
# ACCES_TOKEN_EXPIRE_MINUTES = 30

# fake_users_db = dict(
#     johndoe = dict(
#         username='johndoe',
#         full_name='John Doe',
#         email='johndoe@example.com',
#         hashed_password='',
#         disable=False,
#     )
# )

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     usrtname: str | None = None

# class User(BaseModel):
#     usrname: str
#     email: str | None = None
#     full_name: str | None = None
#     disable: bool = False

# class UserInDB(User):
#     hashed_password: str

# pwd_context = CryptContext(schemes=['bcrypto'], deprecated='auto')

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
    
# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_acccess_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({'exp': expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGOTITHM)
#     return encoded_jwt

# @app.post('/token', response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Incorrect username or password',
#             headers={'WWW-Authenticate': 'Bearer'}
#         )
#     access_token_expires = timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
#     access_token = create_acccess_token(data={'sub': user.usrname}, expires_delta=access_token_expires)
#     return {'access_token': access_token, 'token_type': 'bearer'}

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_expection = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail='Could not validate credentials',
#         headers={'WWW-Authenticate': 'Bearer'},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGOTITHM])
#         username: str = payload('syb')
#         if username in None:
#             raise credentials_expection
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_expection
#     user = get_user(fake_users_db, username=token_data.usrtname)
#     if user is None:
#         raise credentials_expection
#     return user

# async def get_current_activate_user(current_user: User = Depends(get_current_user)):
#     if current_user.disable:
#         raise HTTPException(status_code=400, detail='Inactive User')
#     return current_user

# @app.get('/users/me', response_model=User)
# async def get_me(current_user: User = Depends(get_current_activate_user)):
#     return current_user

# @app.get('/users/me/items')
# async def read_own_items(current_user: User = Depends(get_current_activate_user)):
#     return [{'item_id': 'Foo', 'owner': current_user.usrname}]


# 28 - Middleware and CORS
class MyMiddlewere(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response
    
origin = ['http://localhost:8000', 'http://localhost:3000']
app.add_middleware(MyMiddlewere)
app.add_middleware(CORSMiddleware, allow_origins=origin)

@app.get('/blah')
async def blah():
    return {'hello': 'world'}