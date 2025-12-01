#!/bin/bash

echo "Criando Super Admin..."
python scripts/create_super_user.py

echo "Iniciando Servidor..."
fastapi run app/main.py --port 8000 --host 0.0.0.0
