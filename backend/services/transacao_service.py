# ============================================================
# FinControl – Service: Transacao
# ============================================================

from sqlalchemy.orm import Session
from repositories import transacao_repository, categoria_repository
from schemas.transacao import TransacaoCreate, TransacaoUpdate
from models.transacao import Transacao, TipoEnum
from datetime import date


def listar(
    db: Session,
    user_id: int,
    tipo: TipoEnum | None = None,
    categoria_id: int | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None
) -> list[Transacao]:
    return transacao_repository.listar(
        db=db,
        user_id=user_id,
        tipo=tipo,
        categoria_id=categoria_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


def criar(db: Session, user_id: int, dados: TransacaoCreate) -> Transacao:
    # Verifica se a categoria pertence ao usuário (RN-05)
    categoria = categoria_repository.buscar_por_id(
        db, dados.categoria_id, user_id
    )
    if not categoria:
        raise ValueError("Categoria não encontrada")

    return transacao_repository.criar(
        db=db,
        user_id=user_id,
        dados=dados.model_dump()
    )


def atualizar(
    db: Session,
    transacao_id: int,
    user_id: int,
    dados: TransacaoUpdate
) -> Transacao:
    transacao = transacao_repository.buscar_por_id(db, transacao_id, user_id)
    if not transacao:
        raise ValueError("Transação não encontrada")

    # Verifica categoria se foi alterada (RN-05)
    if dados.categoria_id:
        categoria = categoria_repository.buscar_por_id(
            db, dados.categoria_id, user_id
        )
        if not categoria:
            raise ValueError("Categoria não encontrada")

    return transacao_repository.atualizar(
        db=db,
        transacao=transacao,
        dados=dados.model_dump(exclude_none=True)
    )


def deletar(db: Session, transacao_id: int, user_id: int) -> None:
    transacao = transacao_repository.buscar_por_id(db, transacao_id, user_id)
    if not transacao:
        raise ValueError("Transação não encontrada")

    transacao_repository.deletar(db, transacao)