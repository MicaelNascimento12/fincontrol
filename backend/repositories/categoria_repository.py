# ============================================================
# FinControl – Repository: Categoria
# ============================================================

from sqlalchemy.orm import Session
from models.categoria import Categoria


CATEGORIAS_PADRAO = [
    "Alimentação",
    "Transporte",
    "Saúde",
    "Educação",
    "Moradia",
    "Lazer",
    "Investimentos"
]


def criar_categorias_padrao(db: Session, user_id: int) -> None:
    for nome in CATEGORIAS_PADRAO:
        categoria = Categoria(user_id=user_id, nome=nome)
        db.add(categoria)
    db.commit()


def listar(db: Session, user_id: int) -> list[Categoria]:
    return db.query(Categoria).filter(
        Categoria.user_id == user_id
    ).all()


def buscar_por_id(db: Session, categoria_id: int, user_id: int) -> Categoria | None:
    return db.query(Categoria).filter(
        Categoria.id == categoria_id,
        Categoria.user_id == user_id
    ).first()


def criar(db: Session, user_id: int, nome: str) -> Categoria:
    categoria = Categoria(user_id=user_id, nome=nome)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def atualizar(db: Session, categoria: Categoria, nome: str) -> Categoria:
    categoria.nome = nome
    db.commit()
    db.refresh(categoria)
    return categoria


def deletar(db: Session, categoria: Categoria) -> None:
    db.delete(categoria)
    db.commit()