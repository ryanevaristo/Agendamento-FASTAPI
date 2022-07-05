
from datetime import date, time
from typing import Optional
from pydantic import BaseModel



class AgendamentoSchema(BaseModel):

    id: Optional[int]
    nome_servico: str
    usuario_id: Optional[int]
    ativo: bool = False

    class Config:
        orm_mode = True
    

class AgendamentoSchemaDatas(AgendamentoSchema):
    horas: time | None = None
    created_by: date | None = None
    cancel_date: date | None = None