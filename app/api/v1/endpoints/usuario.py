from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.api.deps import get_current_user, get_session
from app.models.condominio import Condominio
from app.models.usuario import TipoPerfil, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioRead

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario_in: UsuarioCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    query = select(Usuario).where(Usuario.email == usuario_in.email)
    if session.exec(query).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    usuario_dict = usuario_in.model_dump()
    senha_plana = usuario_dict.pop("senha")
    usuario_dict["senha_hash"] = pwd_context.hash(senha_plana)

    if current_user.tipo == TipoPerfil.SUPER_ADMIN:
        pass

    elif current_user.tipo == TipoPerfil.ADMIN:
        usuario_dict["tipo"] = TipoPerfil.MORADOR

        if not current_user.condominio_id:
            raise HTTPException(
                status_code=400,
                detail="Síndico sem condomínio não pode criar moradores.",
            )
        usuario_dict["condominio_id"] = current_user.condominio_id

    else:
        raise HTTPException(
            status_code=403, detail="Você não tem permissão para cadastrar usuários."
        )

    usuario = Usuario.model_validate(usuario_dict)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.get("/", response_model=List[UsuarioRead])
def read_usuarios(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    usuarios = session.exec(select(Usuario).offset(skip).limit(limit)).all()
    return usuarios


@router.get("/me", response_model=UsuarioRead)
def read_user_me(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    user_dict = current_user.model_dump()

    user_response = UsuarioRead.model_validate(user_dict)

    if current_user.condominio_id:
        condominio = session.get(Condominio, current_user.condominio_id)
        if condominio:
            user_response.nome_condominio = condominio.nome

    return user_response


@router.get("/", response_model=List[UsuarioRead])
def list_usuarios(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):

    if current_user.tipo == TipoPerfil.SUPER_ADMIN:
        return session.exec(select(Usuario).offset(skip).limit(limit)).all()

    if current_user.tipo == TipoPerfil.ADMIN:
        if not current_user.condominio_id:
            return []

        query = (
            select(Usuario)
            .where(Usuario.condominio_id == current_user.condominio_id)
            .offset(skip)
            .limit(limit)
        )

        resultados = session.exec(query).all()
        return resultados

    raise HTTPException(status_code=403, detail="Acesso negado.")


@router.patch("/{usuario_id}/toggle-ativo", response_model=UsuarioRead)
def toggle_usuario_ativo(
    usuario_id: str,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    if current_user.tipo not in [TipoPerfil.ADMIN, TipoPerfil.SUPER_ADMIN]:
        raise HTTPException(
            status_code=403, detail="Apenas síndicos podem gerenciar moradores."
        )

    try:
        user_to_update = session.get(Usuario, usuario_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.") from e

    if not user_to_update:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if current_user.tipo == TipoPerfil.ADMIN:
        if user_to_update.condominio_id != current_user.condominio_id:
            raise HTTPException(
                status_code=403, detail="Você não pode gerenciar este usuário."
            )

    user_to_update.ativo = not user_to_update.ativo

    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return user_to_update
