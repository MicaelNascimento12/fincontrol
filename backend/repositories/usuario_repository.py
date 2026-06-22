# ============================================================
# FinControl – Repository: Usuario
# ============================================================

from sqlalchemy.orm import Session
from models.usuario import Usuario


def buscar_por_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def buscar_por_id(db: Session, user_id: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == user_id).first()


def criar(db: Session, nome: str, email: str, senha_hash: str) -> Usuario:
    usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def criar_sem_commit(
    db: Session,
    nome: str,
    email: str,
    senha_hash: str
) -> Usuario:
    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash
    )

    db.add(usuario)
    db.flush()

    return usuario


def atualizar(db: Session, usuario: Usuario, dados: dict) -> Usuario:
    for campo, valor in dados.items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario


def deletar(db: Session, usuario: Usuario) -> None:
    db.delete(usuario)
    db.commit()