from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, col

from app.api.deps import get_session, get_current_user
from app.models.log import LogAcesso
from app.models.usuario import Usuario, TipoPerfil
from app.schemas.log import LogRead

router = APIRouter()

@router.get("/", response_model=List[LogRead])
def read_logs(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.tipo == TipoPerfil.MORADOR:
         raise HTTPException(status_code=403, detail="Acesso negado.")

    query = (
        select(LogAcesso, Usuario)
        .join(Usuario, LogAcesso.usuario_id == Usuario.id)
        .order_by(col(LogAcesso.data_hora).desc())
        .offset(skip)
        .limit(limit)
    )
    
    if current_user.tipo == TipoPerfil.ADMIN:
        query = query.where(Usuario.condominio_id == current_user.condominio_id)

    results = session.exec(query).all()
    
    logs_resposta = []
    for log, usuario in results:
        log_read = LogRead(
            id=log.id,
            data_hora=log.data_hora,
            usuario_id=log.usuario_id,
            portao_id=log.portao_id,
            acao=log.acao,
            sucesso=log.sucesso,
            observacao=log.observacao,
            usuario_nome=usuario.nome
        )
        logs_resposta.append(log_read)
        
    return logs_resposta
