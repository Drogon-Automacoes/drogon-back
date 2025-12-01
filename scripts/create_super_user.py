import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.db import engine, init_db
from app.models.usuario import Usuario, TipoPerfil
from app.models.condominio import Condominio
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_super_user():
    print("Criando o Super Admin...")
    
    init_db()
    
    with Session(engine) as session:
        query = select(Usuario).where(Usuario.email == "super@admin.com")
        user = session.exec(query).first()
        
        if user:
            print("Super Admin já existe!")
            return

        condominio = Condominio(
            nome="Condomínio Matriz (HQ)",
            endereco="Em algum lugar",
            cnpj="00.000.000/0001-00"
        )
        session.add(condominio)
        session.commit()
        session.refresh(condominio)
        print(f"Condomínio criado: {condominio.nome}")

        super_user = Usuario(
            nome="Super Administrador",
            email="super@admin.com",
            senha_hash=pwd_context.hash("123456"),
            tipo=TipoPerfil.SUPER_ADMIN,
            ativo=True,
            condominio_id=condominio.id
        )
        
        session.add(super_user)
        session.commit()
        
        print("\n" + "="*40)
        print("Funcionou")
        print(f"Email: {super_user.email}")
        print(f"Senha: 123456")
        print("="*40 + "\n")

if __name__ == "__main__":
    create_super_user()
