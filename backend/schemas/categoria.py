# ============================================================
# FinControl – Schema: Categoria
# ============================================================

from pydantic import BaseModel, Field, field_validator


class CategoriaCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=80)

    @field_validator("nome")
    @classmethod
    def nome_nao_pode_ser_vazio(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("O nome da categoria é obrigatório")
        return v


class CategoriaUpdate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=80)

    @field_validator("nome")
    @classmethod
    def nome_nao_pode_ser_vazio(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("O nome da categoria é obrigatório")
        return v


class CategoriaResponse(BaseModel):
    id: str
    user_id: str
    nome: str

    class Config:
        from_attributes = True