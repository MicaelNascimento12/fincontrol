# ============================================================
# FinControl – Segurança: Hash de Senha e JWT
# ============================================================

import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verificar_senha(senha: str, hash: str) -> bool:
    return bcrypt.checkpw(
        senha.encode("utf-8"),
        hash.encode("utf-8")
    )


def criar_token(user_id: str) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )

    payload = {
        "sub": user_id,
        "exp": expiracao
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise ValueError("Token inválido")

        return user_id

    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")