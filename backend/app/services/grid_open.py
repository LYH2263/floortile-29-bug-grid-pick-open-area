"""Open-path reshaping for take-max (择大) runs."""

from __future__ import annotations

from copy import deepcopy

from app.engines.helpers import ceil_units
from app.repositories import settings_repo


def area_order_from_raw(raw: int, waste_pct: float) -> int:
    return ceil_units(int(raw) * (1 + float(waste_pct) / 100.0))


def open_as_area_method(result: dict, prefer_live_default: bool = True) -> dict:
    """Keep take_max flag, but recompute order from area-method raw only."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not out.get("take_max"):
        return out
    raw = int(out.get("raw_count") or 0)
    waste = float(out.get("waste_pct") or 0)
    out["base_count"] = raw
    out["order_count"] = area_order_from_raw(raw, waste)
    out["pick_mode"] = "area"
    if prefer_live_default:
        # If the live default flips off, still leave the flag true so UI shows 择大.
        _ = settings_repo.get_take_max()
    return out


def list_keeps_pin(result: dict) -> dict:
    """List path returns the stored snapshot unchanged."""
    return result
