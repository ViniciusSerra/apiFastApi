from fastapi import FastAPI
import uvicorn
from loguru import logger

from src.routers import user_router
from src.routers import auth_router
from src.test import test_database_connection

app = FastAPI()

app.include_router(user_router.router)
app.include_router(auth_router.router)

if __name__ == "__main__":
    teste = test_database_connection()
    if teste is True:
        uvicorn.run(app, host=str("0.0.0.0"), port=int(8001))
        logger.info("API Server iniciado")
    else:
        logger.error("Erro ao iniciar API Server")
