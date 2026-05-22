from pathlib import Path

from pydantic import BaseModel


class AppConfig(BaseModel):
    data_dir: Path = Path("data")
    output_dir: Path = Path("reports")


def get_config() -> AppConfig:
    return AppConfig()
