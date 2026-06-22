# ============================================================
# FinControl – Schema: Transacao
# ============================================================

from pydantic import BaseModel, field_validator
from datetime import date
from enum import Enum


class TipoEnum(str, Enum):
    receita = "receita"
    despesa = "despesa"


class TransacaoCreate(BaseModel):
    categoria_id: int
    tipo: TipoEnum
    valor: float
    data: date
    descricao: str | None = None

    @field_validator("valor")
    @classmethod
    def valor_deve_ser_positivo(cls, v):
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return v

    @field_validator("data")
    @classmethod
    def data_nao_pode_ser_futura(cls, v):
        from datetime import date as date_type
        if v > date_type.today():
            raise ValueError("A data não pode ser futura")
        return v


class TransacaoUpdate(BaseModel):
    categoria_id: int | None = None
    tipo: TipoEnum | None = None
    valor: float | None = None
    data: date | None = None
    descricao: str | None = None


class TransacaoResponse(BaseModel):
    id: int
    user_id: int
    categoria_id: int
    tipo: TipoEnum
    valor: float
    data: date
    descricao: str | None

    class Config:
        from_attributes = True