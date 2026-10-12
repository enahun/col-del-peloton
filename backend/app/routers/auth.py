from fastapi import APIRouter, HTTPException
from app.config import settings

router = APIRouter()


@router.get("/strava/login")
async def strava_login():
    """Redirige al usuario a Strava para autorizar la app."""
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
    """Strava redirige aquí tras la autorización. TODO: implementar."""
    if error:
        raise HTTPException(status_code=400, detail=f"Strava error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Falta el parámetro 'code'")
    # TODO: intercambiar code por access_token, generar JWT, redirigir al frontend
    return {"code_received": code, "status": "pendiente de implementar"}