from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

from app import models, schemas
from app.database import engine, get_db
from app.auth import gerar_hash_senha, verificar_senha, criar_token_acesso

from app.auth import criar_token_acesso, gerar_hash_senha, get_usuario_atual, verificar_senha

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fit Tracker API",
    description="API para acompanhamento de treinos e progressão de carga.",
    version="1.0.0"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/usuarios/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()

    if usuario_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado.")

    senha_criptografada = gerar_hash_senha(usuario.senha)

    novo_usuario = models.Usuario(nome=usuario.nome, email=usuario.email, senha_hash=senha_criptografada)

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post("/login/", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()

    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos.",
        )

    
    access_token = criar_token_acesso(dados={"sub": str(usuario.id)})
    return {"access_token": access_token, "token_type": "bearer"}





@app.post("/exercicios/", response_model=schemas.ExercicioResponse, status_code=status.HTTP_201_CREATED)
def criar_exercicio(exercicio: schemas.ExercicioCreate, db: Session = Depends(get_db)):
    novo_exercicio = models.Exercicio(**exercicio.model_dump())

    db.add(novo_exercicio)
    db.commit()
    db.refresh(novo_exercicio)
    return novo_exercicio

@app.get("/exercicios/", response_model=List[schemas.ExercicioResponse])
def listar_exercicios(db: Session = Depends(get_db)):
    exercicios = db.query(models.Exercicio).all()
    return exercicios


@app.post("/registros", response_model=schemas.RegistroResponse, status_code=status.HTTP_201_CREATED)
def registrar_treino(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == registro.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    exercicio = db.query(models.Exercicio).filter(models.Exercicio.id == registro.exercicio_id).first()
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado.")

    novo_registro = models.RegistroExecucao(
        usuario_id=registro.usuario_id,
        exercicio_id=registro.exercicio_id,
        carga_kg=registro.carga_kg,
        repeticoes=registro.repeticoes
    )
    db.add(novo_registro)
    db.commit()
    db.refresh(novo_registro)
    return novo_registro

@app.get("/registros/usuarios/{usuario_id}", response_model=List[schemas.RegistroResponse])
def obter_registros_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    registros = db.query(models.RegistroExecucao).filter(models.RegistroExecucao.usuario_id == usuario_id).all()
    return registros

@app.get("/usuarios/me", response_model=schemas.UsuarioResponse)
def obter_usuario_logado(usuario_atual: models.Usuario = Depends(get_usuario_atual)):
    return usuario_atual

