# ============================================================
# FinControl – Repository: Transacao
# ============================================================

from sqlalchemy.orm import Session
from models.transacao import Transacao, TipoEnum, StatusEnum
from datetime import date


def listar(
    db: Session,
    user_id: str,
    tipo: TipoEnum | None = None,
    status: StatusEnum | None = None,
    categoria_id: str | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None
) -> list[Transacao]:
    query = db.query(Transacao).filter(Transacao.user_id == user_id)

    if tipo:
        query = query.filter(Transacao.tipo == tipo)
    if status:
        query = query.filter(Transacao.status == status)
    if categoria_id:
        query = query.filter(Transacao.categoria_id == categoria_id)
    if data_inicio:
        query = query.filter(Transacao.data >= data_inicio)
    if data_fim:
        query = query.filter(Transacao.data <= data_fim)

    return query.order_by(Transacao.data.desc()).all()


def buscar_por_id(
    db: Session,
    transacao_id: str,
    user_id: str
) -> Transacao | None:
    return db.query(Transacao).filter(
        Transacao.id == transacao_id,
        Transacao.user_id == user_id
    ).first()


def criar(db: Session, user_id: str, dados: dict) -> Transacao:
    transacao = Transacao(user_id=user_id, **dados)
    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao


def atualizar(db: Session, transacao: Transacao, dados: dict) -> Transacao:
    for campo, valor in dados.items():
        setattr(transacao, campo, valor)

    db.commit()
    db.refresh(transacao)
    return transacao


def deletar(db: Session, transacao: Transacao) -> None:
    db.delete(transacao)
    db.commit()