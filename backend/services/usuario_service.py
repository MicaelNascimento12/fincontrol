# ============================================================
# FinControl – Service: Usuario
# ============================================================

from sqlalchemy.orm import Session
from repositories import usuario_repository
from schemas.usuario import UsuarioUpdate, AlterarSenhaRequest
from models.usuario import Usuario
from core.security import hash_senha, verificar_senha


def obter_perfil(usuario: Usuario) -> Usuario:
    return usuario


def atualizar_perfil(
    db: Session,
    usuario: Usuario,
    dados: UsuarioUpdate
) -> Usuario:
    dados_update = dados.model_dump(exclude_unset=True)

    if "email" in dados_update:
        existente = usuario_repository.buscar_por_email(db, dados_update["email"])

        if existente and existente.id != usuario.id:
            raise ValueError("E-mail já cadastrado")

    if not dados_update:
        return usuario

    return usuario_repository.atualizar(db, usuario, dados_update)


def alterar_senha(
    db: Session,
    usuario: Usuario,
    dados: AlterarSenhaRequest
) -> None:
    if not verificar_senha(dados.senha_atual, usuario.senha_hash):
        raise ValueError("Senha atual incorreta")

    nova_senha_hash = hash_senha(dados.nova_senha)

    usuario_repository.atualizar(
        db,
        usuario,
        {"senha_hash": nova_senha_hash}
    )