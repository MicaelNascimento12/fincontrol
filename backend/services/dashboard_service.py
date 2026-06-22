# ============================================================
# FinControl – Service: Dashboard
# ============================================================

from sqlalchemy.orm import Session
from repositories import dashboard_repository


def obter_resumo(db: Session, user_id: str) -> dict:
    return dashboard_repository.obter_resumo(db, user_id)


def obter_gastos_por_categoria(db: Session, user_id: str) -> list[dict]:
    return dashboard_repository.obter_gastos_por_categoria(db, user_id)


def obter_fluxo_mensal(db: Session, user_id: str) -> list[dict]:
    return dashboard_repository.obter_fluxo_mensal(db, user_id)