from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=6)


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str


class ExercicioCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    grupo_muscular: str = Field(min_length=1, max_length=50)


class ExercicioResponse(ExercicioCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class RegistroCreate(BaseModel):
    exercicio_id: int
    carga_kg: float = Field(ge=0, le=1000)
    repeticoes: int = Field(gt=0, le=1000)


class RegistroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    exercicio_id: int
    carga_kg: float
    repeticoes: int
    data: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
