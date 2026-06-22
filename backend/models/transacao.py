# ============================================================
# FinControl – Model: Transacao
# ============================================================

import enum
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base


class TipoEnum(str, enum.Enum):
    receita = "receita"
    despesa = "despesa"


class Transacao(Base):
    __tablename__ = "transacoes"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    tipo         = Column(Enum(TipoEnum), nullable=False)
    valor        = Column(Numeric(10, 2), nullable=False)
    data         = Column(Date, nullable=False)
    descricao    = Column(String(255), nullable=True)

    usuario   = relationship("Usuario", back_populates="transacoes")
    categoria = relationship("Categoria", back_populates="transacoes")