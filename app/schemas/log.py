from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.log import AcaoPortao


class LogRead(BaseModel):
    id: UUID
    data_hora: datetime
    usuario_id: UUID
    portao_id: UUID
    acao: AcaoPortao
    sucesso: bool
    observacao: str | None = None
    usuario_nome: str | None = "Desconhecido"
