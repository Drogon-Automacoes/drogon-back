from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.api.deps import get_session, get_current_user
from app.models.condominio import Condominio
from app.models.usuario import Usuario, TipoPerfil
from app.schemas.condominio import CondominioCreate, CondominioRead

router = APIRouter()

@router.post("/", response_model=CondominioRead, status_code=201)
def create_condominio(
    condominio_in: CondominioCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.tipo != TipoPerfil.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Apenas Super Admin.")

    condominio = Condominio.model_validate(condominio_in)
    session.add(condominio)
    session.commit()
    session.refresh(condominio)
    return condominio

@router.get("/", response_model=List[CondominioRead])
def list_condominios(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.tipo != TipoPerfil.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Apenas Super Admin.")

    return session.exec(select(Condominio)).all()
