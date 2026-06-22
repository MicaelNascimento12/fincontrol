# ============================================================
# FinControl – Schema: Usuario
# ============================================================

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6, max_length=72)

    @field_validator("nome")
    @classmethod
    def nome_nao_pode_ser_vazio(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("O nome é obrigatório")
        return v


class UsuarioResponse(BaseModel):
    id: str
    nome: str
    email: str
    data_criacao: datetime

    class Config:
        from_attributes = True