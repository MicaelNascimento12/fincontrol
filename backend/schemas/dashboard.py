# ============================================================
# FinControl – Schema: Dashboard
# ============================================================

from pydantic import BaseModel
from decimal import Decimal


class DashboardResumoResponse(BaseModel):
    saldo: Decimal
    receitas: Decimal
    despesas: Decimal


class GastoPorCategoriaResponse(BaseModel):
    categoria: str
    total: Decimal


class FluxoMensalResponse(BaseModel):
    mes: str
    receitas: Decimal
    despesas: Decimal
    saldo: Decimal