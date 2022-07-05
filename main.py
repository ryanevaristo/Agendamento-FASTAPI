
from routers.Pedido import router
from routers.Usuario import router as router_usuario
from routers.Servico import router as router_servico
from fastapi import FastAPI

app = FastAPI()

app.include_router(router=router_usuario,prefix='/usuarios', tags=["Login"])
app.include_router(router=router,prefix='/pedidos', tags=["Pedidos"])
app.include_router(router=router_servico, prefix='/servicos', tags=["Servicos"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0" ,port=8000, reload=True)