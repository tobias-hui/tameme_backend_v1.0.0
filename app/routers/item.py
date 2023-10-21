from fastapi import FastAPI, HTTPException, status, Path
from fastapi.routing import APIRouter
from app.models.item import ItemCreate, ItemUpdate, ItemInDB
from app.core.db import database, items_table

app = APIRouter(tags=["items"])


@app.post("/items/")
async def create_item(item: ItemCreate):
  query = items_table.insert().values(**item.dict())
  last_record_id = await database.execute(query)
  return {**item.dict(), "id": last_record_id}


@app.get("/items/{item_id}/")
async def read_item(item_id: int = Path(...,
                                        title="The ID of the item to get")):
  query = items_table.select().where(items_table.c.id == item_id)
  item = await database.fetch_one(query)
  if item:
    return item
  raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}/")
async def update_item(item_id: int, item: ItemUpdate):
  query = (items_table.update().where(items_table.c.id == item_id).values(
      **item.dict()).returning(items_table))
  updated_item = await database.fetch_one(query)
  if updated_item:
    return updated_item
  raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}/")
async def delete_item(item_id: int):
  query = items_table.delete().where(items_table.c.id == item_id)
  deleted_item = await database.execute(query)
  if deleted_item:
    return {"message": "Item deleted successfully"}
  raise HTTPException(status_code=404, detail="Item not found")
