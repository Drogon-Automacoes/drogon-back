from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import get_session, get_current_user
from app.models.portao import Portao, StatusPortao
from app.models.usuario import Usuario, TipoPerfil
from app.models.log import LogAcesso, AcaoPortao
from app.schemas.portao import PortaoCreate, PortaoRead, PortaoComando

router = APIRouter()


@router.post("/", response_model=PortaoRead, status_code=201)
def create_portao(
    portao_in: PortaoCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.tipo != TipoPerfil.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem cadastrar portões."
        )

    portao_data = portao_in.model_dump()
    portao_data["condominio_id"] = current_user.condominio_id
    portao = Portao.model_validate(portao_data)
    session.add(portao)
    session.commit()
    session.refresh(portao)
    return portao


@router.get("/", response_model=List[PortaoRead])
def list_portoes(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.tipo == TipoPerfil.SUPER_ADMIN:
        return session.exec(select(Portao)).all()
    
    if not current_user.condominio_id:
        return []
        
    query = select(Portao).where(Portao.condominio_id == current_user.condominio_id)
    return session.exec(query).all()

@router.post("/{portao_id}/acionar", response_model=PortaoRead)
def acionar_portao(
    portao_id: str,
    comando: PortaoComando,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    portao = session.get(Portao, portao_id)
    if not portao:
        raise HTTPException(status_code=404, detail="Portão não encontrado")

    if portao.em_manutencao:
        raise HTTPException(status_code=400, detail="Portão em manutenção")

    novo_status = (
        StatusPortao.ABERTO if comando.acao == "abrir" else StatusPortao.FECHADO
    )
    acao_log = AcaoPortao.ABRIR if comando.acao == "abrir" else AcaoPortao.FECHAR

    print(f"--> ENVIANDO COMANDO MQTT: {portao.topico_mqtt} Payload: {comando.acao}")

    portao.status_atual = novo_status
    session.add(portao)

    log = LogAcesso(
        usuario_id=current_user.id,
        portao_id=portao.id,
        acao=acao_log,
        sucesso=True,
        observacao="Acionamento via App",
    )
    session.add(log)

    session.commit()
    session.refresh(portao)
    return portao
