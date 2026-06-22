# ============================================================
# FinControl – Router: Dashboard
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.dependencies import get_usuario_atual
from models.usuario import Usuario
from services import dashboard_service
from schemas.dashboard import (
    DashboardResumoResponse,
    GastoPorCategoriaResponse,
    FluxoMensalResponse
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/resumo",
    response_model=DashboardResumoResponse
)
def obter_resumo(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    return dashboard_service.obter_resumo(db, usuario_atual.id)


@router.get(
    "/gastos-por-categoria",
    response_model=list[GastoPorCategoriaResponse]
)
def obter_gastos_por_categoria(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    return dashboard_service.obter_gastos_por_categoria(db, usuario_atual.id)


@router.get(
    "/fluxo-mensal",
    response_model=list[FluxoMensalResponse]
)
def obter_fluxo_mensal(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    return dashboard_service.obter_fluxo_mensal(db, usuario_atual.id)