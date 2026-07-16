"""Verificacion liviana de ID tokens de Firebase Auth, sin el SDK
firebase-admin completo: ese paquete arrastra google-cloud-firestore,
google-cloud-storage y grpcio (pesados, no usamos nada de eso - solo
verificar un token), y todo indica que ese peso agoto la memoria del
contenedor en Railway (deploy caido tras el primer request).

Firebase firma los ID tokens con RS256 usando certificados publicos que
rotan periodicamente. Verificar la firma no requiere ninguna credencial
de servidor, solo el project_id (no es secreto).
"""

import time

import jwt
import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from app.core.config import settings

CERTS_URL = (
    "https://www.googleapis.com/robot/v1/metadata/x509/"
    "securetoken@system.gserviceaccount.com"
)
ISSUER = f"https://securetoken.google.com/{settings.firebase_project_id}"

_certs_cache: dict[str, object] = {"certs": None, "expires_at": 0.0}


def _get_certs() -> dict[str, str]:
    if _certs_cache["certs"] is None or time.time() > _certs_cache["expires_at"]:
        response = requests.get(CERTS_URL, timeout=5)
        response.raise_for_status()
        _certs_cache["certs"] = response.json()
        _certs_cache["expires_at"] = time.time() + 3600
    return _certs_cache["certs"]  # type: ignore[return-value]


def verify_firebase_token(token: str) -> dict:
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")
    cert_pem = _get_certs().get(kid) if kid else None
    if cert_pem is None:
        raise ValueError("Clave de verificación desconocida")

    cert = x509.load_pem_x509_certificate(cert_pem.encode(), default_backend())
    public_key = cert.public_key()

    return jwt.decode(
        token,
        public_key,  # type: ignore[arg-type]
        algorithms=["RS256"],
        audience=settings.firebase_project_id,
        issuer=ISSUER,
    )
