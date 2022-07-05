
from core.configs import settings
from core.database import engine


async def create_tables() -> None:
    import models.all_models
    print("criando tabelas no banco de dados .....")

    async with engine.begin() as connect:
        await connect.run_sync(settings.DB_BASE_MODEL.metadata.drop_all)
        await connect.run_sync(settings.DB_BASE_MODEL.metadata.create_all)
    
    print("tabelas criada com sucesso !!")


if __name__ == '__main__':
    import asyncio 

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_tables())