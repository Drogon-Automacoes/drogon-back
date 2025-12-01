from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class AcaoPortao(str, Enum):
    ABRIR = "abrir"
    FECHAR = "fechar"
    FORCAR_PARADA = "forcar_parada"


class LogAcesso(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    data_hora: datetime = Field(default_factory=datetime.utcnow)
    usuario_id: UUID = Field(foreign_key="usuario.id")
    portao_id: UUID = Field(foreign_key="portao.id")
    acao: AcaoPortao
    sucesso: bool = True
    observacao: str | None = None
