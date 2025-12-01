from uuid import UUID

from pydantic import BaseModel


class CondominioBase(BaseModel):
    nome: str
    endereco: str | None = None
    cnpj: str | None = None


class CondominioCreate(CondominioBase):
    pass


class CondominioRead(CondominioBase):
    id: UUID
