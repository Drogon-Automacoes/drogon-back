from sqlmodel import SQLModel, create_engine

from app.core.configs import settings
from app.models.condominio import Condominio  # noqa: F401
from app.models.log import LogAcesso  # noqa: F401
from app.models.portao import Portao  # noqa: F401
from app.models.usuario import Unidade, Usuario  # noqa: F401

engine = create_engine(settings.DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
