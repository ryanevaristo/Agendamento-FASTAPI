
from datetime import date, time
from typing import Optional
from pydantic import BaseModel



class PedidoSchema(BaseModel):
    id: Optional[int]
    usuario_id: Optional[int]
    servico_id: Optional[int]
    num_pedido: int | None = None
    ativo: bool = False

    class Config:
        orm_mode = True
    

class PedidoSchemaDatas(PedidoSchema):
    horas: time | None = None
    created_by: date | None = None
    cancel_date: date | None = None