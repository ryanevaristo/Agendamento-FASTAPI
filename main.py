
from routers.Agenda import router
from routers.Usuario import router as router_usuario
from fastapi import FastAPI

app = FastAPI()

app.include_router(router=router,prefix='/agenda', tags=["Agendamento"])
app.include_router(router=router_usuario,prefix='/usuarios', tags=["Login"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0" ,port=8000, reload=True)