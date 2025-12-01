from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class TipoPerfil(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MORADOR = "morador"
    PORTEIRO = "porteiro"


class Unidade(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    bloco: str
    numero: str
    condominio_id: UUID = Field(foreign_key="condominio.id")

    moradores: List["Usuario"] = Relationship(back_populates="unidade")


class Usuario(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    nome: str
    email: str = Field(unique=True, index=True)
    senha_hash: str
    tipo: TipoPerfil = Field(default=TipoPerfil.MORADOR)
    ativo: bool = Field(default=True)
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
    unidade_id: Optional[UUID] = Field(default=None, foreign_key="unidade.id")
    unidade: Optional[Unidade] = Relationship(back_populates="moradores")
    condominio_id: Optional[UUID] = Field(default=None, foreign_key="condominio.id")
    condominio: Optional["Condominio"] = Relationship(back_populates="usuarios")
