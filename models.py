from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: str


class PedidoCreate(BaseModel):
    producto_id: str
    cantidad: int

class PedidoResponse(BaseModel):
    id: str
    producto_id: str
    cantidad: int
    fecha: datetime
    estado: str = "pendiente"