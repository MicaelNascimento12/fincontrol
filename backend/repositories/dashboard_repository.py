# ============================================================
# FinControl – Repository: Dashboard
# ============================================================

from sqlalchemy.orm import Session
from sqlalchemy import func, case
from models.transacao import Transacao, TipoEnum, StatusEnum
from models.categoria import Categoria


def obter_resumo(db: Session, user_id: str) -> dict:
    resultado = db.query(
        func.coalesce(
            func.sum(
                case(
                    (Transacao.tipo == TipoEnum.receita, Transacao.valor),
                    else_=0
                )
            ),
            0
        ).label("receitas"),
        func.coalesce(
            func.sum(
                case(
                    (Transacao.tipo == TipoEnum.despesa, Transacao.valor),
                    else_=0
                )
            ),
            0
        ).label("despesas")
    ).filter(
        Transacao.user_id == user_id,
        Transacao.status == StatusEnum.pago
    ).first()

    receitas = resultado.receitas or 0
    despesas = resultado.despesas or 0

    return {
        "saldo": receitas - despesas,
        "receitas": receitas,
        "despesas": despesas
    }


def obter_gastos_por_categoria(db: Session, user_id: str) -> list[dict]:
    resultados = db.query(
        Categoria.nome.label("categoria"),
        func.coalesce(func.sum(Transacao.valor), 0).label("total")
    ).join(
        Transacao,
        Transacao.categoria_id == Categoria.id
    ).filter(
        Transacao.user_id == user_id,
        Transacao.tipo == TipoEnum.despesa,
        Transacao.status == StatusEnum.pago
    ).group_by(
        Categoria.nome
    ).order_by(
        func.sum(Transacao.valor).desc()
    ).all()

    return [
        {
            "categoria": item.categoria,
            "total": item.total
        }
        for item in resultados
    ]


def obter_fluxo_mensal(db: Session, user_id: str) -> list[dict]:
    resultados = db.query(
        func.date_format(Transacao.data, "%Y-%m").label("mes"),
        func.coalesce(
            func.sum(
                case(
                    (Transacao.tipo == TipoEnum.receita, Transacao.valor),
                    else_=0
                )
            ),
            0
        ).label("receitas"),
        func.coalesce(
            func.sum(
                case(
                    (Transacao.tipo == TipoEnum.despesa, Transacao.valor),
                    else_=0
                )
            ),
            0
        ).label("despesas")
    ).filter(
        Transacao.user_id == user_id,
        Transacao.status == StatusEnum.pago
    ).group_by(
        func.date_format(Transacao.data, "%Y-%m")
    ).order_by(
        func.date_format(Transacao.data, "%Y-%m")
    ).all()

    return [
        {
            "mes": item.mes,
            "receitas": item.receitas,
            "despesas": item.despesas,
            "saldo": item.receitas - item.despesas
        }
        for item in resultados
    ]