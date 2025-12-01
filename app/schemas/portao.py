from uuid import UUID

from pydantic import BaseModel

from app.models.portao import StatusPortao


class PortaoBase(BaseModel):
    nome: str
    descricao: str | None = None
    topico_mqtt: str
    em_manutencao: bool = False


class PortaoCreate(PortaoBase):
    pass


class PortaoRead(PortaoBase):
    id: UUID
    status_atual: StatusPortao


class PortaoUpdate(BaseModel):
    nome: str | None = None
    em_manutencao: bool | None = None


class PortaoComando(BaseModel):
    acao: str
