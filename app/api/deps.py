from typing import Generator
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlmodel import Session

from app.core.configs import settings
from app.db import engine
from app.models.usuario import Usuario

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login"
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(reusable_oauth2)
) -> Usuario:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
        
        if token_data is None:
            raise JWTError("Token sem sub")
            
        user_id = UUID(token_data)
        
    except (JWTError, ValidationError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credenciais inválidas",
        )
    
    user = session.get(Usuario, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return user

def get_current_user_optional(
    session: Session = Depends(get_session),
    token: str = Depends(reusable_oauth2)
) -> Usuario | None:
    try:
        return get_current_user(session, token)
    except:
        return None
