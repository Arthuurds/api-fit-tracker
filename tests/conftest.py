import os
import tempfile

import pytest

# Usa um banco SQLite temporário, separado do banco de desenvolvimento.
_arquivo_banco = os.path.join(tempfile.mkdtemp(), "teste.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_arquivo_banco}"

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def criar_usuario_e_logar(client, email="arthur@email.com", senha="senha123"):
    client.post("/usuarios/", json={"nome": "Arthur", "email": email, "senha": senha})
    resposta = client.post("/login/", data={"username": email, "password": senha})
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
