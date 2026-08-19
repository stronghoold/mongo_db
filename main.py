from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from datetime import datetime
from typing import List

from database import productos_collection, pedidos_collection
from models import (
    ProductoCreate, ProductoResponse,
    PedidoCreate, PedidoResponse
)

app = FastAPI(
    title="API REST - Clase 2",
    description="CRUD de productos y gestión de pedidos con FastAPI y MongoDB",
    version="1.0.0"
)

def fix_id(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@app.get("/")
def home():
    return {"mensaje": "API funcional de la Clase 2"}


@app.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate):
    nuevo = producto.model_dump()
    resultado = await productos_collection.insert_one(nuevo)
    doc = await productos_collection.find_one({"_id": resultado.inserted_id})
    return fix_id(doc)

@app.get("/productos", response_model=List[ProductoResponse])
async def obtener_productos():
    productos = []
    async for doc in productos_collection.find():
        productos.append(fix_id(doc))
    return productos

@app.get("/productos/{id}", response_model=ProductoResponse)
async def obtener_producto_por_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    doc = await productos_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return fix_id(doc)

@app.put("/productos/{id}", response_model=ProductoResponse)
async def actualizar_producto(id: str, producto: ProductoCreate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    resultado = await productos_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": producto.model_dump()}
    )
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    doc = await productos_collection.find_one({"_id": ObjectId(id)})
    return fix_id(doc)

@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    resultado = await productos_collection.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None


@app.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def crear_pedido(pedido: PedidoCreate):
    if not ObjectId.is_valid(pedido.producto_id):
        raise HTTPException(status_code=400, detail="ID de producto no válido")
    
    prod = await productos_collection.find_one({"_id": ObjectId(pedido.producto_id)})
    if not prod:
        raise HTTPException(status_code=404, detail="El producto no existe")

    nuevo_pedido = {
        "producto_id": pedido.producto_id,
        "cantidad": pedido.cantidad,
        "fecha": datetime.now(),
        "estado": "pendiente"
    }
    resultado = await pedidos_collection.insert_one(nuevo_pedido)
    doc = await pedidos_collection.find_one({"_id": resultado.inserted_id})
    return fix_id(doc)

@app.get("/pedidos", response_model=List[PedidoResponse])
async def obtener_pedidos():
    pedidos = []
    async for doc in pedidos_collection.find():
        pedidos.append(fix_id(doc))
    return pedidos