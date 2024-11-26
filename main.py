from enum import Enum
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()

# СКЛАДСКОЙ УЧЁТ

class Categories(Enum):
    electronics = "электроника"
    clothes = "одежда"
    food = "продукты"
    tools = "инструменты"
    books = "книги"
    toys = "игрушки"


class Item(BaseModel):
    id: int
    category: Categories
    name: str
    price: float
    code: int
    quantity: int


STORAGE = [
    {
        "id": 1,
        "category": "одежда",
        "name": "Джинсы",
        "price": 3500,
        "code": 856149325746,
        "quantity": 23,
    },
    {
        "id": 2,
        "category": "электроника",
        "name": "Блендер",
        "price": 5200,
        "code": 856149325746,
        "quantity": 184,
    },
    {
        "id": 3,
        "category": "инструменты",
        "name": "Молоток",
        "price": 1800,
        "code": 856149325746,
        "quantity": 527,
    },
]


@app.get("/items")
async def items() -> list[dict]:
    return STORAGE


@app.get("/items/{item_id}")
async def item(item_id: int) -> dict:
    item = next((i for i in STORAGE if i['id'] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail='Товар не найден.')
    return item


@app.post("/items/add_json", status_code=status.HTTP_201_CREATED)
async def add_json_item(item: Item) -> Item:
    item.id = max(i["id"] for i in STORAGE) + 1 if STORAGE else 1
    STORAGE.append(item.model_dump())
    return item


@app.post("/items/add", status_code=status.HTTP_201_CREATED)
async def add_item(category: Categories, name: str, price: int, code: int, quantity: int) -> Item:
    item = Item(id=max(i["id"] for i in STORAGE) + 1 if STORAGE else 1, category=category, name=name, price=price, code=code, quantity=quantity)
    STORAGE.append(item.model_dump())
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, updated_item: Item) -> Item:
    index = next((index for index, i in enumerate(STORAGE) if i["id"] == item_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден")
    updated_item.id = item_id
    STORAGE[index] = updated_item.model_dump()
    return updated_item


@app.put("/items/update_quantity/{item_id}")
async def update_item_quantity(item_id: int, quantity: int):
    item = next((i for i in STORAGE if i['id'] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail='Товар не найден.')
    item.update(quantity=quantity)
    index = next(index for index, i in enumerate(STORAGE) if i["id"] == item_id)
    STORAGE[index] = item
    return item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    index = next((index for index, i in enumerate(STORAGE) if i["id"] == item_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден")
    STORAGE.pop(index)
    return {"detail": "Товар удалён успешно."}