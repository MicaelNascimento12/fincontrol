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


class UsuarioUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None

    @field_validator("nome")
    @classmethod
    def nome_nao_pode_ser_vazio(cls, v):
        if v is None:
            return v

        v = v.strip()
        if not v:
            raise ValueError("O nome não pode ser vazio")
        return v


class AlterarSenhaRequest(BaseModel):
    senha_atual: str = Field(..., min_length=6, max_length=72)
    nova_senha: str = Field(..., min_length=6, max_length=72)


class UsuarioResponse(BaseModel):
    id: str
    nome: str
    email: str
    data_criacao: datetime

    class Config:
        from_attributes = True