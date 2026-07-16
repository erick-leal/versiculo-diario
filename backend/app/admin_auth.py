from fastapi import Header, HTTPException
from firebase_admin import auth as firebase_auth

from app.firebase import firebase_app  # noqa: F401 - fuerza la inicializacion de la app de Firebase


def require_admin(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta el token de administrador")

    token = authorization.removeprefix("Bearer ")
    try:
        return firebase_auth.verify_id_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")
