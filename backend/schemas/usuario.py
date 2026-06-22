# ============================================================
# FinControl – Schema: Usuario
# ============================================================

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    data_criacao: datetime

    class Config:
        from_attributes = True