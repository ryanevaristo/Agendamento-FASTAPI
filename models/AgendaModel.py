from datetime import time
from core.configs import settings
from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Date, Time
from sqlalchemy.orm import relationship



class AgendaModel(settings.DB_BASE_MODEL):
    __tablename__ = 'agendas'

    id: int = Column(Integer, primary_key= True, autoincrement=True)
    nome_servico: str = Column(String(256), nullable=True)
    horas: time = Column(Time, nullable=True)
    ativo: bool = Column(Boolean, default=False)
    created_by = Column(Date, nullable=True)
    cancel_date = Column(Date, nullable=True)
    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'))
    criador: relationship = relationship("UsuarioModel", back_populates='agendas', lazy='joined')