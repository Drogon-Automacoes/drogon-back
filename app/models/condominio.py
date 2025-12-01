from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional

class Condominio(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    nome: str
    endereco: str | None = None
    usuarios: List["Usuario"] = Relationship(back_populates="condominio")
    portoes: List["Portao"] = Relationship(back_populates="condominio")
