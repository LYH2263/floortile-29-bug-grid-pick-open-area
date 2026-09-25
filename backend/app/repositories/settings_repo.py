from app.config import DEFAULT_TAKE_MAX, DEFAULT_WASTE_PCT
from app.db import connect

_TRUE_VALUES = {"1", "true", "yes", "on"}


def get_all() -> dict:
    conn = connect()
    try:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        out = {r["key"]: r["value"] for r in rows}
        if "waste_pct" not in out:
            out["waste_pct"] = str(DEFAULT_WASTE_PCT)
        if "take_max" not in out:
            out["take_max"] = "1" if DEFAULT_TAKE_MAX else "0"
        return out
    finally:
        conn.close()


def get_waste_pct() -> float:
    raw = get_all().get("waste_pct", str(DEFAULT_WASTE_PCT))
    return float(raw)


def get_take_max() -> bool:
    raw = get_all().get("take_max", "1" if DEFAULT_TAKE_MAX else "0")
    return str(raw).strip().lower() in _TRUE_VALUES


def set_values(values: dict) -> None:
    conn = connect()
    try:
        for key, value in values.items():
            conn.execute(
                """
                INSERT INTO settings(key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
                """,
                (key, str(value)),
            )
        conn.commit()
    finally:
        conn.close()
