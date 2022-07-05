from core.configs import settings
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship




class UsuarioModel(settings.DB_BASE_MODEL):
    __tablename__ = 'usuarios'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome : str = Column(String(256), nullable=True)
    foto: str = Column(String, nullable=True)
    sobrenome : str = Column(String(256), nullable=True)
    telefone : str = Column(String(256), nullable=True)
    email : str = Column(String(256),index=True, nullable=False, unique=True)
    senha : str = Column(String(256), nullable=False)
    is_admin: bool = Column(Boolean(), default=False)
    pedidos: relationship = relationship(
        "PedidoModel",
        cascade="all,delete-orphan",
        back_populates="criador",
        uselist=True,
        lazy="joined"
    )