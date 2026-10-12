from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    strava_client_id: str
    strava_client_secret: str
    strava_redirect_uri: str

    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"

    session_secret: str = "cambiame_en_produccion"
    session_cookie_name: str = "cdp_session"
    session_max_age: int = 60 * 60 * 24 * 7  # 7 días

    class Config:
        env_file = ".env"


settings = Settings()