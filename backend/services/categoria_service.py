# ============================================================
# FinControl – Service: Categoria
# ============================================================

from sqlalchemy.orm import Session
from repositories import categoria_repository, transacao_repository
from schemas.categoria import CategoriaCreate, CategoriaUpdate
from models.categoria import Categoria


def listar(db: Session, user_id: int) -> list[Categoria]:
    return categoria_repository.listar(db, user_id)


def criar(db: Session, user_id: int, dados: CategoriaCreate) -> Categoria:
    return categoria_repository.criar(db, user_id, dados.nome)


def atualizar(
    db: Session,
    categoria_id: int,
    user_id: int,
    dados: CategoriaUpdate
) -> Categoria:
    categoria = categoria_repository.buscar_por_id(db, categoria_id, user_id)
    if not categoria:
        raise ValueError("Categoria não encontrada")

    return categoria_repository.atualizar(db, categoria, dados.nome)


def deletar(db: Session, categoria_id: int, user_id: int) -> None:
    categoria = categoria_repository.buscar_por_id(db, categoria_id, user_id)
    if not categoria:
        raise ValueError("Categoria não encontrada")

    # RN-04: bloqueia exclusão se houver transações vinculadas
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