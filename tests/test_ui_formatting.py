import importlib.util
from decimal import Decimal
from pathlib import Path


def _load_home_module():
    path = Path("app/ui/Home.py")
    spec = importlib.util.spec_from_file_location("home_ui", path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_format_rate_accepts_decimal_and_string_values() -> None:
    module = _load_home_module()

    assert module._format_rate(Decimal("0.1511")) == "15.11%"
    assert module._format_rate("0.1511") == "15.11%"
