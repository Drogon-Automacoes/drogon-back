from fastapi import APIRouter
from app.api.v1.endpoints import usuario, login, portao, log, condominio

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(usuario.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(portao.router, prefix="/portoes", tags=["portoes"])
api_router.include_router(log.router, prefix="/logs", tags=["logs"])
api_router.include_router(condominio.router, prefix="/condominios", tags=["condominios"])
