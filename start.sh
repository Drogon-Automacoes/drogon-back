#!/bin/bash

set -e

echo "Iniciando o deploy no render"

echo "Verificando Super Admin..."
python scripts/create_super_user.py || echo "Aviso: Script de criação retornou erro (talvez usuário já exista). Seguindo..."

echo "Subindo o Servidor Uvicorn..."
exec fastapi run app/main.py --port 8000 --host 0.0.0.0
