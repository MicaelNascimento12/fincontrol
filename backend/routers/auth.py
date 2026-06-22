# ============================================================
# FinControl – Router: Autenticação
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.usuario import UsuarioCreate, UsuarioResponse
from schemas.auth import LoginRequest, TokenResponse
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/cadastro", response_model=TokenResponse, status_code=201)
def cadastrar(dados: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return auth_service.cadastrar(db, dados)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.login(db, dados.email, dados.senha)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )