# ============================================================
# FinControl – Service: Categoria
# ============================================================

from sqlalchemy.orm import Session
from repositories import categoria_repository, transacao_repository
from schemas.categoria import CategoriaCreate, CategoriaUpdate
from models.categoria import Categoria


def listar(db: Session, user_id: str) -> list[Categoria]:
    return categoria_repository.listar(db, user_id)


def criar(db: Session, user_id: str, dados: CategoriaCreate) -> Categoria:
    existente = categoria_repository.buscar_por_nome(db, user_id, dados.nome)
    if existente:
        raise ValueError("Você já possui uma categoria com esse nome")

    return categoria_repository.criar(db, user_id, dados.nome)


def atualizar(
    db: Session,
    categoria_id: str,
    user_id: str,
    dados: CategoriaUpdate
) -> Categoria:
    categoria = categoria_repository.buscar_por_id(db, categoria_id, user_id)
    if not categoria:
        raise ValueError("Categoria não encontrada")

    existente = categoria_repository.buscar_por_nome(db, user_id, dados.nome)
    if existente and existente.id != categoria.id:
        raise ValueError("Você já possui uma categoria com esse nome")

    return categoria_repository.atualizar(db, categoria, dados.nome)


def deletar(db: Session, categoria_id: str, user_id: str) -> None:
    categoria = categoria_repository.buscar_por_id(db, categoria_id, user_id)
    if not categoria:
        raise ValueError("Categoria não encontrada")

    transacoes = transacao_repository.listar(
        db=db,
        user_id=user_id,
        categoria_id=categoria_id
    )

    if transacoes:
        raise ValueError(
            "Categoria possui transações vinculadas. "
            "Reatribua as transações para outra categoria antes de excluir"
        )

    categoria_repository.deletar(db, categoria)