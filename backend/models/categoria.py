# ============================================================
# FinControl – Model: Categoria
# ============================================================

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id      = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nome    = Column(String(80), nullable=False)

    usuario    = relationship("Usuario", back_populates="categorias")
    transacoes = relationship("Transacao", back_populates="categoria")