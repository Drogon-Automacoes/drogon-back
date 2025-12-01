import pytest
from fastapi.testclient import TestClient
from app.models.portao import StatusPortao

def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Sistema Online"

def test_create_user_and_login(client: TestClient):
    response = client.post("/api/v1/usuarios/", json={
        "nome": "Test User",
        "email": "test@example.com",
        "senha": "password123",
        "tipo": "admin"
    })
    assert response.status_code == 201
    
    login_response = client.post("/api/v1/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

@pytest.mark.parametrize("nome_portao, topico, deve_funcionar", [
    ("Portao A", "bloco/a", True),
    ("Portao B", "bloco/b", True),
])
def test_criar_portoes(client: TestClient, nome_portao, topico, deve_funcionar):
    client.post("/api/v1/usuarios/", json={"nome":"Adm","email":"adm@t.com","senha":"123","tipo":"admin"})
    token = client.post("/api/v1/login", data={"username":"adm@t.com","password":"123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/api/v1/portoes/", headers=headers, json={
        "nome": nome_portao,
        "topico_mqtt": topico,
        "em_manutencao": False
    })
    
    if deve_funcionar:
        assert response.status_code == 201
        assert response.json()["nome"] == nome_portao
