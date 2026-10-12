import httpx

STRAVA_API = "https://www.strava.com/api/v3"
STRAVA_OAUTH = "https://www.strava.com/oauth/token"


async def exchange_code_for_token(code: str, client_id: str, client_secret: str) -> dict:
    """Intercambia el 'code' de OAuth por access_token y refresh_token."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            STRAVA_OAUTH,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
            },
        )
        resp.raise_for_status()
        return resp.json()


async def get_athlete_activities(access_token: str, per_page: int = 10) -> list[dict]:
    """Obtiene las últimas actividades del atleta autenticado."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{STRAVA_API}/athlete/activities",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"per_page": per_page},
        )
        resp.raise_for_status()
        return resp.json()