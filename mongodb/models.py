from pydantic import BaseModel, field
from typing import list, Optional

class producto(basemodel):
    noombre: str = field(..., example="teclado mecanico")
    description: Optional[str] = field(None, example="teclado rgbswitch azul")
    precio: float = field(..., gt=0, example=49.99)
    stock: int = field(..., ge=0, example=10)
    
class Itemlpedido(basemodel):
       producto_id: str
       cantidad: int = field(...,gt=0, example=2)
       
class pepido(basemodel):
    cliente: str = field(..., example="Juan Perez")
    items: list[Itemlpedido]
    total: float = field(..., gt=0, example=99.98)
    estado: str = field(default="pendiente", example="pendiente")