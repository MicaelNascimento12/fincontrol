# ============================================================
# FinControl – Service: Autenticação
# ============================================================

from sqlalchemy.orm import Session
from core.security import hash_senha, verificar_senha, criar_token
from repositories import usuario_repository, categoria_repository
from schemas.usuario import UsuarioCreate


def cadastrar(db: Session, dados: UsuarioCreate) -> dict:
    # RN-01: e-mail já cadastrado
    existente = usuario_repository.buscar_por_email(db, dados.email)
    if existente:
        raise ValueError("E-mail já cadastrado")

    # RNF-01: senha criptografada com bcrypt
    senha_hash = hash_senha(dados.senha)

    # Cria o usuário
    usuario = usuario_repository.criar(
        db=db,
        nome=dados.nome,
        email=dados.email,
        senha_hash=senha_hash
    )

    # RF-16 e RN-08: copia categorias padrão para o novo usuário
    categoria_repository.criar_categorias_padrao(db, usuario.id)

    # RF-03: gera token JWT
    token = criar_token(usuario.id)

    return {"access_token": token, "token_type": "bearer"}


def login(db: Session, email: str, senha: str) -> dict:
    # Busca usuário pelo e-mail
    usuario = usuario_repository.buscar_por_email(db, email)

    # Mensagem genérica por segurança (UC-04 fluxo A1 e A2)
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        raise ValueError("E-mail ou senha inválidos")

    # RF-03: gera token JWT
    token = criar_token(usuario.id)

    return {"access_token": token, "token_type": "bearer"}