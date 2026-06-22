# ============================================================
# FinControl – Model: Categoria
# ============================================================

import uuid
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    nome = Column(String(80), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "nome", name="UK_categorias_usuario_nome"),
    )

    usuario = relationship("Usuario", back_populates="categorias")
    transacoes = relationship("Transacao", back_populates="categoria")