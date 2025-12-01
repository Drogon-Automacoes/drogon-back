from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.usuario import TipoPerfil


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo: TipoPerfil = TipoPerfil.MORADOR
    ativo: bool = True
    unidade_id: UUID | None = None
    condominio_id: UUID | None = None


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioRead(UsuarioBase):
    id: UUID
    nome_condominio: str | None = None


class UsuarioUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None
    ativo: bool | None = None
    condominio_id: UUID | None = None
