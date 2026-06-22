# ============================================================
# FinControl – Schema: Transacao
# ============================================================

from pydantic import BaseModel, Field, field_validator
from datetime import date
from enum import Enum
from decimal import Decimal


class TipoEnum(str, Enum):
    receita = "receita"
    despesa = "despesa"


class StatusEnum(str, Enum):
    pendente = "pendente"
    pago = "pago"
    cancelado = "cancelado"


class TransacaoCreate(BaseModel):
    categoria_id: str
    tipo: TipoEnum
    status: StatusEnum = StatusEnum.pago
    valor: Decimal = Field(..., gt=0)
    data: date
    descricao: str | None = Field(default=None, max_length=255)
    observacao: str | None = None

    @field_validator("categoria_id")
    @classmethod
    def categoria_id_obrigatorio(cls, v):
        if not v or not v.strip():
            raise ValueError("A categoria é obrigatória")
        return v.strip()

    @field_validator("data")
    @classmethod
    def data_nao_pode_ser_futura(cls, v):
        if v > date.today():
            raise ValueError("A data não pode ser futura")
        return v

    @field_validator("descricao")
    @classmethod
    def descricao_limpa(cls, v):
        if v is None:
            return v
        v = v.strip()
        return v or None

    @field_validator("observacao")
    @classmethod
    def observacao_limpa(cls, v):
        if v is None:
            return v
        v = v.strip()
        return v or None


class TransacaoUpdate(BaseModel):
    categoria_id: str | None = None
    tipo: TipoEnum | None = None
    status: StatusEnum | None = None
    valor: Decimal | None = Field(default=None, gt=0)
    data: date | None = None
    descricao: str | None = Field(default=None, max_length=255)
    observacao: str | None = None

    @field_validator("categoria_id")
    @classmethod
    def categoria_id_nao_pode_ser_vazio(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError("A categoria não pode ser vazia")
        return v.strip()

    @field_validator("data")
    @classmethod
    def data_nao_pode_ser_futura(cls, v):
        if v is None:
            return v
        if v > date.today():
            raise ValueError("A data não pode ser futura")
        return v

    @field_validator("descricao")
    @classmethod
    def descricao_limpa(cls, v):
        if v is None:
            return v
        v = v.strip()
        return v or None

    @field_validator("observacao")
    @classmethod
    def observacao_limpa(cls, v):
        if v is None:
            return v
        v = v.strip()
        return v or None


class TransacaoResponse(BaseModel):
    id: str
    user_id: str
    categoria_id: str
    tipo: TipoEnum
    status: StatusEnum
    valor: Decimal
    data: date
    descricao: str | None
    observacao: str | None

    class Config:
        from_attributes = True