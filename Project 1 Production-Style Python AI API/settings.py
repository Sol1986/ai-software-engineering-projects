from functools import lru_cache  # tool so you can cache a function’s result.

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Software Engineering Foundations"
    environment: str = "development"
    log_level: str = "INFO"
    llm_provider: str = "openai"
    llm_model: str = "gpt-5.6-luna"
    llm_api_key: str | None = None # “llm_api_key can be a string or None, and its default value is None.”

    # “Configure this settings class to read variables from a .env file using UTF-8 text, and ignore any extra variables it does not recognize.”
    model_config = SettingsConfigDict(env_file = ".env", env_file_encoding = "utf-8", extra = "ignore")



# Decorators are lines beginning with @ placed directly above a function or class. They add behavior to it without changing the code inside the function.
# “Cache the result of get_settings so repeated calls can reuse it.”
@lru_cache # “This decorator caches the result of the function so that subsequent calls with the same arguments return the cached result instead of recomputing it.”
def get_settings() -> Settings:
    """Get the application settings, caching the result for efficiency."""
    return Settings() 

