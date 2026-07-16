from fastapi import Header, HTTPException

from app.firebase_verify import verify_firebase_token


def require_admin(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta el token de administrador")

    token = authorization.removeprefix("Bearer ")
    try:
        return verify_firebase_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
