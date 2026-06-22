# ============================================================
# FinControl – Router: Transacoes
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from core.dependencies import get_usuario_atual
from models.usuario import Usuario
from models.transacao import TipoEnum
from schemas.transacao import TransacaoCreate, TransacaoUpdate, TransacaoResponse
from services import transacao_service
from datetime import date

router = APIRouter(prefix="/transacoes", tags=["Transações"])


@router.get("/", response_model=list[TransacaoResponse])
def listar(
    tipo: TipoEnum | None = Query(default=None),
    categoria_id: str | None = Query(default=None),
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    return transacao_service.listar(
        db=db,
        user_id=usuario.id,
        tipo=tipo,
        categoria_id=categoria_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


@router.post("/", response_model=TransacaoResponse, status_code=201)
def criar(
    dados: TransacaoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    try:
        return transacao_service.criar(db, usuario.id, dados)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{transacao_id}", response_model=TransacaoResponse)
def atualizar(
    transacao_id: str,
    dados: TransacaoUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    try:
        return transacao_service.atualizar(db, transacao_id, usuario.id, dados)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{transacao_id}", status_code=204)
def deletar(
    transacao_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    try:
        transacao_service.deletar(db, transacao_id, usuario.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )