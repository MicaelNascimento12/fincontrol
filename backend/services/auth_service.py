# ============================================================
# FinControl – Service: Autenticação
# ============================================================

from sqlalchemy.orm import Session
from core.security import hash_senha, verificar_senha, criar_token
from repositories import usuario_repository, categoria_repository
from schemas.usuario import UsuarioCreate


def cadastrar(db: Session, dados: UsuarioCreate) -> dict:
    existente = usuario_repository.buscar_por_email(db, dados.email)

    if existente:
        raise ValueError("E-mail já cadastrado")

    senha_hash = hash_senha(dados.senha)

    try:
        usuario = usuario_repository.criar_sem_commit(
            db=db,
            nome=dados.nome,
            email=dados.email,
            senha_hash=senha_hash
        )

        categoria_repository.criar_categorias_padrao(db, usuario.id)

        db.commit()
        db.refresh(usuario)

    except Exception as e:
        db.rollback()
        print("ERRO AO CADASTRAR USUÁRIO:", e)
        raise ValueError(f"Erro ao cadastrar usuário: {e}")

    token = criar_token(usuario.id)

    return {"access_token": token, "token_type": "bearer"}

def login(db: Session, email: str, senha: str) -> dict:
    usuario = usuario_repository.buscar_por_email(db, email)

    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        raise ValueError("E-mail ou senha inválidos")

    token = criar_token(usuario.id)

    return {"access_token": token, "token_type": "bearer"}