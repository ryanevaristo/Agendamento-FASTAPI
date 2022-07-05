from typing import List

from fastapi import APIRouter, Response, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.AgendaModel import AgendaModel
from models.UsuarioModel import UsuarioModel
from schemas.AgendaSchema import AgendamentoSchemaDatas
from core.deps import get_session, get_current_user


router = APIRouter()

#POST Agenda
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AgendamentoSchemaDatas)
async def post_agenda(Agenda: AgendamentoSchemaDatas, db: AsyncSession = Depends(get_session)):
    novo_Agenda: AgendaModel = AgendaModel(
        nome_servico=Agenda.nome_servico, horas=Agenda.horas ,created_by=Agenda.created_by, cancel_date=Agenda.cancel_date, usuario_id=Agenda.usuario_id )

    db.add(novo_Agenda)
    await db.commit()

    return novo_Agenda


#GET DATAS
@router.get('/',response_model=List[AgendamentoSchemaDatas])
async def get_Agendas(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AgendaModel)
        result = await session.execute(query)
        Agendas: List[AgendaModel] = result.scalars().unique().all()
        
        if Agendas:
            return Agendas
        else:
            raise HTTPException(detail="Agenda não Encontrado", status_code=status.HTTP_404_NOT_FOUND)


#GET Agenda
@router.get('/{id_agenda}', response_model=AgendamentoSchemaDatas, status_code=status.HTTP_200_OK)
async def get_Agenda(id_agenda: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AgendaModel).filter(AgendaModel.id == id_agenda)
        result = await session.execute(query)
        Agenda: AgendaModel = result.scalars().unique().one_or_none()

        if Agenda:
            return Agenda
        else:
            raise HTTPException(detail="Agenda não Encontrado", status_code=status.HTTP_404_NOT_FOUND)



#PUT Agenda
@router.put('/{id_agenda}', response_model=AgendamentoSchemaDatas, status_code=status.HTTP_202_ACCEPTED)
async def put_Agenda(id_agenda: int, Agenda: AgendamentoSchemaDatas, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(AgendaModel).filter(AgendaModel.id == id_agenda).filter(UsuarioModel.id == usuario_logado.id)
        result = await session.execute(query)
        Agenda_up: AgendaModel = result.scalars().unique().one_or_none()

        if Agenda_up:
            if Agenda.nome_servico:
                Agenda_up.nome_servico = Agenda.nome_servico
            if Agenda.horas:
                Agenda_up.horas = Agenda.horas
            if Agenda.created_by:
                Agenda_up.created_by = Agenda.created_by
            if Agenda.cancel_date:
                Agenda_up.cancel_date = Agenda.cancel_date

            await session.commit()
            return Agenda_up
        else:
            raise HTTPException(detail="Agenda não Encontrado", status_code=status.HTTP_404_NOT_FOUND)



#DELETE Agenda
@router.delete('/{id_agenda}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_Agenda(id_agenda: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AgendaModel).filter(AgendaModel.id == id_agenda)
        result = session.execute(query)
        Agenda_del: AgendaModel = result.scalars().unique().one_or_none()

        if Agenda_del:
            await session.delete(Agenda_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Agenda não Encontrado", status_code=status.HTTP_404_NOT_FOUND)
