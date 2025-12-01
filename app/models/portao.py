from enum import Enum
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

class StatusPortao(str, Enum):
    ABERTO = "aberto"
    FECHADO = "fechado"
    ERRO = "erro"
    DESCONECTADO = "desconectado"

class Portao(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    nome: str
    descricao: str | None = None
    topico_mqtt: str = Field(unique=True)
    status_atual: StatusPortao = Field(default=StatusPortao.FECHADO)
    em_manutencao: bool = Field(default=False)

    condominio_id: UUID = Field(foreign_key="condominio.id")
    condominio: Optional["Condominio"] = Relationship(back_populates="portoes")
