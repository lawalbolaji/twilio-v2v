from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY: str
    TWILIO_AUTH_TOKEN: str
    PORT: str = "8080"
