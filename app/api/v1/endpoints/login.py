from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Any

from app.api.deps import get_session
from app.core.security import create_access_token, verify_password
from app.models.usuario import Usuario
from app.schemas.token import Token

router = APIRouter()


@router.post("/login", response_model=Token)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Any:
    query = select(Usuario).where(Usuario.email == form_data.username)
    usuario = session.exec(query).first()

    if not usuario or not verify_password(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    if not usuario.ativo:
        raise HTTPException(status_code=400, detail="Sua conta foi bloqueada pelo síndico. Entre em contato com a administração.")

    return {
        "access_token": create_access_token(usuario.id),
        "token_type": "bearer",
    }
