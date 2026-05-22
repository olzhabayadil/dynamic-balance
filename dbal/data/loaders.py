from pathlib import Path
from typing import Any

import pandas as pd  # type: ignore[import-untyped]

from dbal.products.deal import Deal


def load_deals_csv(path: str | Path) -> list[Deal]:
    frame = pd.read_csv(path)
    return [_deal_from_row(row) for row in frame.to_dict(orient="records")]


def _deal_from_row(row: dict[str, Any]) -> Deal:
    return Deal.model_validate(row)
