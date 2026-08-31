"""Environment-backed configuration."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings with safe local defaults."""

    model_config = SettingsConfigDict(env_prefix="SAFEOPSBENCH_")
    db_url: str = "sqlite+pysqlite:///:memory:"
    results_dir: Path = Path("results")
    log_level: str = "INFO"
    random_seed: int = 42
