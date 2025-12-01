from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlmodel import Session

from app.models.condominio import Condominio
from app.models.usuario import TipoPerfil, Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(name="setup_data")
def setup_data_fixture(session: Session):
    condominio = Condominio(nome="Condomínio Teste", cnpj="000")
    session.add(condominio)
    session.commit()
    session.refresh(condominio)

    super_admin = Usuario(
        nome="Super Teste",
        email="super@test.com",
        senha_hash=pwd_context.hash("123"),
        tipo=TipoPerfil.SUPER_ADMIN,
        condominio_id=condominio.id,
        ativo=True,
    )
    session.add(super_admin)
    session.commit()

    return {"condominio_id": str(condominio.id)}


def test_create_sindico_flow(client: TestClient, setup_data):
    login_resp = client.post(
        "/api/v1/login", data={"username": "super@test.com", "password": "123"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    condo_id = setup_data["condominio_id"]
    resp = client.post(
        "/api/v1/usuarios/",
        headers=headers,
        json={
            "nome": "Síndico Teste",
            "email": "sindico@test.com",
            "senha": "123",
            "tipo": "admin",
            "condominio_id": condo_id,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["email"] == "sindico@test.com"


@pytest.mark.parametrize(
    "nome_portao, topico",
    [
        ("Portao A", "bloco/a"),
        ("Portao B", "bloco/b"),
    ],
)
def test_criar_portoes_sindico(
    client: TestClient, session: Session, setup_data, nome_portao, topico
):

    condo_id = UUID(setup_data["condominio_id"])

    sindico = Usuario(
        nome="Sindico",
        email=f"sindico_{topico}@test.com",
        senha_hash=pwd_context.hash("123"),
        tipo=TipoPerfil.ADMIN,
        condominio_id=condo_id,
        ativo=True,
    )
    session.add(sindico)
    session.commit()

    login_resp = client.post(
        "/api/v1/login", data={"username": sindico.email, "password": "123"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/v1/portoes/",
        headers=headers,
        json={"nome": nome_portao, "topico_mqtt": topico, "em_manutencao": False},
    )

    assert response.status_code == 201
    assert response.json()["nome"] == nome_portao


def test_root_welcome(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "Sistema Online" in response.json()["message"]


def test_docs_exist(client: TestClient):
    response = client.get("/docs")
    assert response.status_code == 200
