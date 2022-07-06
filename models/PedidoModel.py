from datetime import time
from core.configs import settings
from sqlalchemy import Boolean, Column, ForeignKey,select, func, Integer, Date, Time
from sqlalchemy.orm import relationship



class PedidoModel(settings.DB_BASE_MODEL):
    __tablename__ = 'pedidos'

    id: int = Column(Integer, primary_key= True, autoincrement=True)
    servico_id: int = Column(Integer, ForeignKey('servicos.id'))
    usuario_id: int = Column(Integer ,ForeignKey('usuarios.id'))
    num_pedido: int = Column(Integer, nullable=True)
    horas: time = Column(Time, nullable=True)
    ativo: bool = Column(Boolean, default=False)
    created_by = Column(Date, nullable=True)
    cancel_date = Column(Date, nullable=True)
    criador: relationship = relationship("UsuarioModel", back_populates='pedidos', lazy='joined')


# count criado para num_pedido
variavel = select([func.count()]).select_from(PedidoModel)
