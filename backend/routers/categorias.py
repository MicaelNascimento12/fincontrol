# ============================================================
# FinControl – Router: Categorias
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from core.dependencies import get_usuario_atual
from models.usuario import Usuario
from schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from services import categoria_service

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=list[CategoriaResponse])
def listar(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    return categoria_service.listar(db, usuario.id)


@router.post("/", response_model=CategoriaResponse, status_code=201)
def criar(
    dados: CategoriaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    return categoria_service.criar(db, usuario.id, dados)


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar(
    categoria_id: str,
    dados: CategoriaUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    try:
        return categoria_service.atualizar(db, categoria_id, usuario.id, dados)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{categoria_id}", status_code=204)
def deletar(
    categoria_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    try:
        categoria_service.deletar(db, categoria_id, usuario.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )