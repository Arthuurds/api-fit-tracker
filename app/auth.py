import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app import models
from app.database import get_db

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-troque-em-producao")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)

def criar_token_acesso(dados: dict) -> str:
    dados_token = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_token.update({"exp": expiracao})
    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.Usuario:
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise credenciais_invalidas
    except JWTError:
        raise credenciais_invalidas

    usuario = db.query(models.Usuario).filter(models.Usuario.id == int(usuario_id)).first()
    if usuario is None:
        raise credenciais_invalidas
    return usuario
