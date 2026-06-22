# ============================================================
# FinControl – Schema: Categoria
# ============================================================

from pydantic import BaseModel


class CategoriaCreate(BaseModel):
    nome: str


class CategoriaUpdate(BaseModel):
    nome: str


class CategoriaResponse(BaseModel):
    id: int
    user_id: int
    nome: str

    class Config:
        from_attributes = True