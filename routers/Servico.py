from typing import List

from fastapi import APIRouter, Response, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.ServicoModel import ServicoModel
from models.UsuarioModel import UsuarioModel
from core.deps import get_session, get_current_user
from schemas.ServicoSchema import ServicoSchema


router = APIRouter()

#POST servico
@router.post('/', status_code=status.HTTP_201_CREATED)
async def post_servico(servico: ServicoSchema,usuario_logado: UsuarioModel = Depends(get_current_user),db: AsyncSession = Depends(get_session)):
    novo_servico: ServicoModel = ServicoModel(
        id=servico.id,
        nome_servico=servico.nome_servico,
        valor=servico.valor,
        tempo=servico.tempo
        )

    db.add(novo_servico)
    await db.commit()

    return novo_servico


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


#GET servico
@router.get('/{id_servico}', status_code=status.HTTP_200_OK)
async def get_servico(id_servico: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel).filter(ServicoModel.id == id_servico)
        result = await session.execute(query)
        servico: ServicoSchema = result.scalars().unique().one_or_none()

        if servico:
            return servico
        else:
            raise HTTPException(detail="Serviço não Encontrado", status_code=status.HTTP_404_NOT_FOUND)


#GET servico
@router.put('/{id_servico}', status_code=status.HTTP_202_ACCEPTED)
async def put_servico(servico: ServicoSchema,id_servico: int,usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel).filter(ServicoModel.id == id_servico).filter(ServicoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        servico_up: ServicoSchema = result.scalars().unique().one_or_none()

        if servico_up:
            if servico.nome_servico:
                servico_up.nome_servico = servico.nome_servico
            if servico.valor:
                servico_up.valor = servico.valor
            if servico.tempo:
                servico_up.tempo = servico.tempo

            await session.commit()
            return servico_up
        else:
            raise HTTPException(detail="Serviço não Encontrado", status_code=status.HTTP_404_NOT_FOUND)


#DELETE Serviço
@router.delete('/{id_servico}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_servico(id_servico: int, usuario_logado: UsuarioModel = Depends(get_current_user),db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ServicoModel).filter(ServicoModel.id == id_servico).filter(ServicoModel.usuario_id == usuario_logado)
        result = session.execute(query)
        servico_del: ServicoSchema = result.scalars().unique().one_or_none()

        if servico_del:
            await session.delete(servico_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Serviço não Encontrado", status_code=status.HTTP_404_NOT_FOUND)
