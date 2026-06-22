# ============================================================
# FinControl – Model: Usuario
# ============================================================

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id           = Column(Integer, primary_key=True, index=True)
    nome         = Column(String(100), nullable=False)
    email        = Column(String(150), nullable=False, unique=True)
    senha_hash   = Column(String(255), nullable=False)
    data_criacao = Column(DateTime, server_default=func.now())

    categorias = relationship(
        "Categoria",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    transacoes = relationship(
        "Transacao",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )