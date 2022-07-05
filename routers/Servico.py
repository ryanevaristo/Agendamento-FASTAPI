from typing import List

from fastapi import APIRouter, Response, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.ServicoModel import ServicoModel
from models.UsuarioModel import UsuarioModel
from core.deps import get_session, get_current_user


router = APIRouter()



#GET serviços
@router.get('/')
async def get_servicos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel)
        result = await session.execute(query)
        servicos: List[ServicoModel] = result.scalars().unique().all()
        
        if servicos:
            return servicos
        else:
            raise HTTPException(detail="Serviço não Encontrado", status_code=status.HTTP_404_NOT_FOUND)




#DELETE Serviço
@router.delete('/{id_servico}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_servico(id_servico: int, usuario_logado: UsuarioModel = Depends(get_current_user),db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel).filter(ServicoModel.id == id_servico).filter(ServicoModel.usuario_id == usuario_logado)
        result = session.execute(query)
        servico_del: ServicoModel = result.scalars().unique().one_or_none()

        if servico_del:
            await session.delete(servico_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Serviço não Encontrado", status_code=status.HTTP_404_NOT_FOUND)
