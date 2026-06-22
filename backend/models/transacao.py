# ============================================================
# FinControl – Model: Transacao
# ============================================================

import uuid
import enum
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from database import Base


class TipoEnum(str, enum.Enum):
    receita = "receita"
    despesa = "despesa"


class StatusEnum(str, enum.Enum):
    pendente = "pendente"
    pago = "pago"
    cancelado = "cancelado"


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    categoria_id = Column(String(36), ForeignKey("categorias.id"), nullable=False)

    tipo = Column(Enum(TipoEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.pago)

    valor = Column(Numeric(10, 2), nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String(255), nullable=True)
    observacao = Column(Text, nullable=True)

    usuario = relationship("Usuario", back_populates="transacoes")
    categoria = relationship("Categoria", back_populates="transacoes")