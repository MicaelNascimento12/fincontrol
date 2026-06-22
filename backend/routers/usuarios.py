# ============================================================
# FinControl – Router: Usuario
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from core.dependencies import get_usuario_atual
from models.usuario import Usuario
from services import usuario_service
from schemas.usuario import (
    UsuarioResponse,
    UsuarioUpdate,
    AlterarSenhaRequest
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.get("/me", response_model=UsuarioResponse)
def obter_perfil(
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    return usuario_service.obter_perfil(usuario_atual)


@router.put("/me", response_model=UsuarioResponse)
def atualizar_perfil(
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    try:
        return usuario_service.atualizar_perfil(db, usuario_atual, dados)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/me/senha", status_code=status.HTTP_204_NO_CONTENT)
def alterar_senha(
    dados: AlterarSenhaRequest,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    try:
        usuario_service.alterar_senha(db, usuario_atual, dados)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )