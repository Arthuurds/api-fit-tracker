from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_atributes = True

class ExercicioCreate(BaseModel):
    nome: str
    grupo_muscular: str

class ExercicioResponse(ExercicioCreate):
    id: int

    class Config:
        from_atributes = True

class RegistroCreate(BaseModel):
    usuario_id: int
    exercicio_id: int
    carga_kg: float
    repeticoes: int

class RegistroResponse(BaseModel):
    id: int
    usuario_id: int
    exercicio_id: int
    carga_kg: float
    repeticoes: int
    data: datetime

    class Config:
        from_atributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"