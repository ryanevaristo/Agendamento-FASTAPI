from core.configs import settings
from sqlalchemy import Column, String, ForeignKey, Integer


class ServicoModel(settings.DB_BASE_MODEL):
    __tablename__ = 'servicos'


    id = Column(Integer, autoincrement=True, primary_key=True)
    nome_servico = Column(String(256), nullable=True)
    valor = Column(Integer, nullable=True)
    tempo = Column(String(256), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))