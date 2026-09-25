"""Floor tile order count: area method + optional grid layout preview."""

from app.engines.helpers import ceil_units


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    take_max: bool = False,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    base_count: raw_count, or max(raw_count, grid_count) when take_max is on
    order_count: ceil(base_count * (1 + waste_pct/100))
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    base = max(raw, layout["grid_count"]) if take_max else raw
    with_waste = ceil_units(base * (1 + float(waste_pct) / 100.0))
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "take_max": bool(take_max),
        "base_count": base,
        "order_count": with_waste,
        "layout": layout,
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method)."""
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
