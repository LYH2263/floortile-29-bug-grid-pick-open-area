from fastapi import APIRouter
from pydantic import BaseModel

from app.repositories import settings_repo

router = APIRouter(tags=["settings"])


class SettingsUpdate(BaseModel):
    waste_pct: float | None = None
    take_max: bool | None = None


@router.get("/settings")
def get_settings():
    return settings_repo.get_all()


@router.post("/settings")
def update_settings(body: SettingsUpdate):
    values = {}
    if body.waste_pct is not None:
        values["waste_pct"] = str(body.waste_pct)
    if body.take_max is not None:
        values["take_max"] = "1" if body.take_max else "0"
    if values:
        settings_repo.set_values(values)
    return settings_repo.get_all()
