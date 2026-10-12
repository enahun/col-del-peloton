from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from app.config import settings
from app.services import strava

router = APIRouter()

# Serializador para firmar/verificar la cookie de sesión
serializer = URLSafeTimedSerializer(settings.session_secret, salt="cdp-session")


def create_session_cookie(data: dict) -> str:
    """Firma un dict como cookie de sesión."""
    return serializer.dumps(data)


def read_session_cookie(value: str) -> dict | None:
    """Verifica y deserializa la cookie. Devuelve None si inválida/expirada."""
    try:
        return serializer.loads(value, max_age=settings.session_max_age)
    except (BadSignature, SignatureExpired):
        return None


@router.get("/strava/login")
async def strava_login():
    """Devuelve la URL a la que el frontend debe redirigir al usuario."""
    scope = "activity:read_all"
    url = (
        "https://www.strava.com/oauth/authorize"
        f"?client_id={settings.strava_client_id}"
        f"&redirect_uri={settings.strava_redirect_uri}"
        f"&response_type=code"
        f"&approval_prompt=auto"
        f"&scope={scope}"
    )
    return {"authorize_url": url}


@router.get("/strava/callback")
async def strava_callback(code: str | None = None, error: str | None = None):
    """Strava redirige aquí tras la autorización."""
    if error:
        raise HTTPException(status_code=400, detail=f"Strava error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Falta el parámetro 'code'")

    # 1. Intercambiar code por tokens
    try:
        token_data = await strava.exchange_code_for_token(
            code=code,
            client_id=settings.strava_client_id,
            client_secret=settings.strava_client_secret,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error con Strava: {e}")

    # 2. Construir payload de sesión
    session_data = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "expires_at": token_data["expires_at"],
        "athlete_id": token_data["athlete"]["id"],
        "athlete_name": f"{token_data['athlete']['firstname']} {token_data['athlete']['lastname']}",
    }

    # 3. Redirigir al frontend con la cookie firmada
    response = RedirectResponse(url=f"{settings.frontend_url}/dashboard")
    response.set_cookie(
        key=settings.session_cookie_name,
        value=create_session_cookie(session_data),
        max_age=settings.session_max_age,
        httponly=True,
        secure=True,        # solo HTTPS (Render ya es HTTPS)
        samesite="lax",     # permite la redirección desde Strava
    )
    return response


@router.get("/me")
async def me(request: Request):
    """Devuelve info del atleta autenticado (para que el frontend sepa quién está logueado)."""
    cookie = request.cookies.get(settings.session_cookie_name)
    if not cookie:
        raise HTTPException(status_code=401, detail="No autenticado")
    data = read_session_cookie(cookie)
    if not data:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")
    return {
        "athlete_id": data["athlete_id"],
        "athlete_name": data["athlete_name"],
    }


@router.post("/logout")
async def logout():
    """Cierra sesión borrando la cookie."""
    response = RedirectResponse(url=settings.frontend_url)
    response.delete_cookie(settings.session_cookie_name)
    return response