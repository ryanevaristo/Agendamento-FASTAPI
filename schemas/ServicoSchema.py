from pydantic import BaseModel
from typing import Optional


class ServicoSchema(BaseModel):
    id: Optional[int]
    nome_servico: str
    valor: int
    tempo: str

    class Config:
        orm_mode = True
        