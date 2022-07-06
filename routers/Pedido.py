from typing import List

from fastapi import APIRouter, Response, status, Depends, HTTPException


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy import func


from models.PedidoModel import PedidoModel, variavel
from models.UsuarioModel import UsuarioModel
from schemas.PedidoSchema import PedidoSchemaDatas
from core.deps import get_session, get_current_user

router = APIRouter()



#POST pedido
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PedidoSchemaDatas)
async def post_pedido(pedido: PedidoSchemaDatas,usuario_logado: UsuarioModel = Depends(get_current_user),db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = variavel.where(PedidoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        num_pedido1 = result.scalar()
        print(num_pedido1)
        novo_pedido: PedidoModel = PedidoModel(
            id=pedido.id,
            usuario_id=pedido.usuario_id, 
            servico_id=pedido.servico_id, 
            num_pedido=num_pedido1,
            ativo=pedido.ativo,
            horas=pedido.horas,
            created_by=pedido.created_by, 
            cancel_date=pedido.cancel_date)
        
        if pedido.usuario_id == usuario_logado.id:
            db.add(novo_pedido)
            await db.commit()
            return novo_pedido
        else:
            raise HTTPException(detail="Você não está autorizado", status_code=status.HTTP_401_UNAUTHORIZED)


#GET Pedidos
@router.get('/',response_model=List[PedidoSchemaDatas])
async def get_pedidos(db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(PedidoModel)
        result = await session.execute(query)
        pedidos: List[PedidoSchemaDatas] = result.scalars().unique().all()
        
        if pedidos:
            return pedidos
        else:
            raise HTTPException(detail="Pedido não Encontrado", status_code=status.HTTP_404_NOT_FOUND)


#GET Pedido
@router.get('/{id_pedido}', response_model=PedidoSchemaDatas, status_code=status.HTTP_200_OK)
async def get_pedido(id_pedido: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PedidoModel).filter(PedidoModel.id == id_pedido)
        result = await session.execute(query)
        pedido: PedidoSchemaDatas = result.scalars().unique().one_or_none()

        if pedido:
            return pedido
        else:
            raise HTTPException(detail="Pedido não Encontrado", status_code=status.HTTP_404_NOT_FOUND)



#DELETE Pedido
@router.delete('/{id_pedido}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pedido(id_pedido: int, usuario_logado: UsuarioModel = Depends(get_current_user),db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PedidoModel).filter(PedidoModel.id == id_pedido).filter(PedidoModel.usuario_id == usuario_logado)
        result = session.execute(query)
        pedido_del: PedidoSchemaDatas = result.scalars().unique().one_or_none()

        if pedido_del:
            await session.delete(pedido_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Pedido não Encontrado", status_code=status.HTTP_404_NOT_FOUND)
